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
from courses.models import Unit
from django.db.models.functions import Coalesce
from django.db.models import Prefetch, Count, Sum, OuterRef, Exists, Subquery, IntegerField, Q, FloatField

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
            courses = Category.objects.get(id=category_id).course_set.prefetch_related(
            'tags', 'categories__course_set', 'privacy__shared_with'
            ).select_related('privacy').all()

        except Category.DoesNotExist:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)


        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
