from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CourseEnrollmentSerializer
from courses.utils import get_course, allowed_to_access_course
import alteby.utils as general_utils

class CoursesEnrollments(APIView):

    def get(self, request, user_id, format=None):
        if request.user.id == user_id:
            enrollments = request.user.enrollments.all()
            serializer = CourseEnrollmentSerializer(enrollments, many=True)
            return Response(serializer.data)
        response = general_utils.error('page_access_denied')
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, user_id, format=None):
        try:
            request_body = request.data
            course = request_body['course']
            request_body['user'] = user_id

        except Exception as e:
            return Response(general_utils.error('required_fields'), status=status.HTTP_400_BAD_REQUEST)

        course, found, error = get_course(course)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if not allowed_to_access_course(request.user, course):
            return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

        serializer = CourseEnrollmentSerializer(data=request_body, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(general_utils.success('enrolled'), status=status.HTTP_201_CREATED)
