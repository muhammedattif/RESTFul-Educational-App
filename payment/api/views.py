from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CourseEnrollmentSerializer

class CoursesEnrollments(APIView):

    def get(self, request, user_id, format=None):
        if request.user.id == user_id:
            enrollments = request.user.courses_enrollments.all()
            serializer = CourseEnrollmentSerializer(enrollments, many=True)
            return Response(serializer.data)
        response = general_utils.error('page_access_denied')
        return Response(response, status=status.HTTP_403_FORBIDDEN)
