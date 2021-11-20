from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer
from courses.api.serializers import CourseSerializer
from categories.models import Category


class CategoryList(APIView, PageNumberPagination):
    """
    List all categories.
    """
    def get(self, request, format=None):
        categories = Category.objects.all()
        categories = self.paginate_queryset(categories, request, view=self)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryFilter(APIView, PageNumberPagination):

    def get(self, request, category_id, format=None):
        courses = Category.objects.get(id=category_id).course_set.all()
        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)