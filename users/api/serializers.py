from django.contrib.auth import authenticate
from users.models import User, Student
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction

class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic
    def save(self):
        is_student = False
        is_teacher = False
        if 'user_type' in self.validated_data:
            if self.validated_data['user_type'] == 'student':
                is_student = True
            elif self.validated_data['user_type'] == 'teacher':
                is_teacher = True
        else:
            is_student = True

        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            is_student=is_student,
            is_teacher=is_teacher
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password does not match.'})
        user.set_password(password)
        user.save()
        return user





class AuthTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if not validateEmail(email_or_username):
                try:
                    user_request = User.objects.get(username=email_or_username)
                except User.DoesNotExist:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError({
                        'status': 'error',
                        'message': msg
                    })

                email_or_username = user_request.email

            user = authenticate(email=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError({
                        'status': 'error',
                        'message': msg
                    })
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError({
                    'status': 'error',
                    'message': msg
                })
        else:
            msg = 'Must include "email or username" and "password"'
            raise serializers.ValidationError({
                'status': 'error',
                'message': msg
            })

        attrs['user'] = user
        return attrs


def validateEmail( email ):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    year_in_school = serializers.CharField(source='get_year_in_school_display')
    academic_year = serializers.CharField(source='get_academic_year_display')
    class Meta:
        model = Student
        fields = '__all__'
