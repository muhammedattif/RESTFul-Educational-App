from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import renderers
from rest_framework import parsers
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.http import JsonResponse
from .serializers import AuthTokenSerializer, SignUpSerializer, StudentSerializer, ChangePasswordSerializer
from django.core.exceptions import ValidationError
from users.models import Student
from courses.api.serializers import CourseSerializer
from courses.models import Course
from users.models import User
from rest_framework.permissions import IsAuthenticated
from django_rest_passwordreset.views import ResetPasswordConfirm
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import pre_password_reset, post_password_reset
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django_rest_passwordreset.serializers import ResetTokenSerializer
from rest_framework import exceptions
from django.conf import settings
from django.shortcuts import render

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


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(ResetPasswordConfirm):

    def get(self, request):
        token = request.GET.get('token', None)
        data = {'token': token}

        try:
            if not token:
                raise Exception("Invalid Link.")
            serializer = ResetTokenSerializer(data=data)
            serializer.is_valid(raise_exception=False)
            return render(request, 'users/reset_password_confirm.html')
        except Exception as e:
            context = {
            'error_message': 'This link may be invalid or expired.'
            }
            return render(request, 'users/reset_password_error.html', context)



    def post(self, request, *args, **kwargs):
        data = {
        'token': request.GET.get('token'),
        'password': request.data['password']
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        # change users password (if we got to this code it means that the user is_active)
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            try:
                # validate the password against existing validators
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                # raise a validation error for the serializer
                return render(request, 'users/reset_password_confirm.html')
                # raise exceptions.ValidationError({
                #     'password': e.messages
                # })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})


class ProfileDetail(APIView):

    def get(self, request):
        student = Student.objects.select_related('user').get(user=request.user)
        serializer = StudentSerializer(student, many=False)
        context = serializer.data
        return Response(serializer.data)

class EnrolledCourses(APIView):

    def get(self, request, user_id):
        courses_ids = request.user.enrollments.values_list('course', flat=True)
        courses = Course.objects.filter(id__in=courses_ids)
        serializer = CourseSerializer(courses, many=True, context={'request':request})
        context = serializer.data
        return Response(serializer.data)
