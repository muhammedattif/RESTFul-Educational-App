from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import renderers
from rest_framework import parsers
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.http import JsonResponse
from .serializers import AuthTokenSerializer, SignUpSerializer, StudentSerializer
from django.core.exceptions import ValidationError
from users.models import Student
from courses.api.serializers import CourseSerializer
from courses.models import Course

class SignIn(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            content = {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'year_in_school': user.student_info.year_in_school,
                'academic_year': user.student_info.academic_year,
                'major': user.student_info.major
            }

            return Response(content)
        except:
            response = {}
            errors = serializer.errors
            for error in errors:
                response[error] = errors[error][0]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class SignUp(APIView):
    permission_classes = ()
    def post(self, request, format=True):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'year_in_school': user.student_info.year_in_school,
                'academic_year': user.student_info.academic_year,
                'major': user.student_info.major
            }
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)

class ProfileDetail(APIView):

    def get(self, request):
        student = Student.objects.get(user=request.user)
        serializer = StudentSerializer(student, many=False)
        context = serializer.data
        return Response(serializer.data)

class EnrolledCourses(APIView):

    def get(self, request, user_id):
        courses_ids = request.user.enrollments.values_list('course', flat=True)
        courses = Course.objects.filter(id__in=courses_ids)
        serializer = CourseSerializer(courses, many=True)
        context = serializer.data
        return Response(serializer.data)
