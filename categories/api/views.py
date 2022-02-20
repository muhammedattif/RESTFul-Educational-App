from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer
from courses.api.serializers import CourseSerializer
from categories.models import Category
import alteby.utils as general_utils


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
            courses = Category.objects.prefetch_related('course_set','course_set__content', 'course_set__categories__course_set').get(id=category_id).course_set.all()
        except Category.DoesNotExist:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)


        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
