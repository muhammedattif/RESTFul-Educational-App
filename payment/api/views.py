from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializers import CourseEnrollmentSerializer

class CoursesEnrollments(APIView):

    def get(self, request, user_id, format=None):
        if request.user.id == user_id:
            enrollments = request.user.courses_enrollments.all()
            serializer = CourseEnrollmentSerializer(enrollments, many=True)
            return Response(serializer.data)
        response = {
            'status': 'error',
            'message': 'Access denied!',
            'error_description': 'You don\'t have access to preview this page.'
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)
