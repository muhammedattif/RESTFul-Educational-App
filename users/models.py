from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models import F
from django.db import transaction

# this class is for overriding default users manager of django user model
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_staff=False, is_superuser=False, is_teacher=False, is_student=True):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise VlaueError('User must have a username')

        user = self.model(
                        email=self.normalize_email(email),
                        username=username,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        is_teacher=is_teacher,
                        is_student=is_student
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            is_staff = True,
            is_superuser = True,
            is_teacher = True
        )
        user.save(using = self._db)
        return user

# Account Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True, validators=[UnicodeUsernameValidator()])
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_active = models.BooleanField('Active status', default=True)
    is_staff = models.BooleanField('Staff status', default=False)
    is_teacher = models.BooleanField('Teacher status', default=False)
    is_student = models.BooleanField('Student status', default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # resize profile image before saving
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)


class Student(models.Model):

    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    ACADEMIC_YEAR = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
        (7, 'Seventh'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="student_info")
    major = models.CharField(blank=True, null=True, max_length=40)
    academic_year = models.IntegerField(blank=True, null=True, choices=ACADEMIC_YEAR)
    year_in_school = models.CharField(max_length=20, blank=True, null=True, choices=YEAR_IN_SCHOOL_CHOICES)

    def __str__(self):
        return self.user.email

    def is_enrolled(self, course):
        return course.id in self.user.enrollments.values_list('course', flat=True)

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="teacher_info")
    major = models.CharField(blank=True, max_length=40)

    def __str__(self):
        return self.user.email
