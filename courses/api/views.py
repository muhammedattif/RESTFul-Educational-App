from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializers import CourseSerializer
from courses.models import Course
from django.db.models import Q
from functools import reduce
import operator

class CourseList(APIView, PageNumberPagination):

    def get(self, request, format=None):

        request_params = request.GET
        if request_params:
            search_query = request_params.get('q').split(" ")
            query = reduce(operator.or_, (Q(title__icontains=search_term) | Q(description__icontains=search_term) for search_term in search_query))
            courses = Course.objects\
                .prefetch_related('content__quiz__questions__choices', 'content__privacy', 'categories', 'privacy__shared_with')\
                .filter(query)
        else:
            courses = Course.objects.prefetch_related('content__quiz__questions__choices', 'content__privacy', 'categories', 'privacy__shared_with')

        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetail(APIView, PageNumberPagination):

    def get(self, request, course_id, format=None):
        course = Course.objects.prefetch_related('content__quiz__questions__choices').get(id=course_id)
        if course.can_access(request.user):
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)
        response = {
            'status': 'error',
            'message': 'Access denied!',
            'error_description': 'You don\'t have access to this resourse!, enroll this course to see its content.'
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)
