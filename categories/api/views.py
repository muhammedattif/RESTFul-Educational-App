from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer
from courses.api.serializers import CourseSerializer
from categories.models import Category
import alteby.utils as general_utils
from django.db.models import Count, Sum, OuterRef, Exists, Subquery, IntegerField, Q
from payment.models import CourseEnrollment

class CategoryList(APIView, PageNumberPagination):
    """
    List all categories.
    """
    def get(self, request, format=None):
        categories = Category.objects.all().prefetch_related('course_set')
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryFilter(APIView, PageNumberPagination):

    def get(self, request, category_id, format=None):
        try:
            courses = Category.objects.get(id=category_id).course_set.prefetch_related('tags', 'categories__course_set', 'privacy__shared_with').select_related('privacy').annotate(
                units_count=Count('units', distinct=True)
            ).annotate(
                lectures_count=Count('units__topics__lectures', distinct=True)
            ).annotate(
                duration=Sum('units__topics__lectures__duration', distinct=True)
            ).annotate(
                is_enrolled=Exists(CourseEnrollment.objects.filter(course=OuterRef('pk'), user=self.request.user))
            ).annotate(
                lectures_viewed_count=Count('activity', filter=Q(activity__user=self.request.user), distinct=True)
            )

        except Category.DoesNotExist:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)


        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
