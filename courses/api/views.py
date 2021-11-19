from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import CourseSerializer
from courses.models import Course

@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.prefetch_related('content__quiz__questions__choices')
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course(request, course_id):
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
