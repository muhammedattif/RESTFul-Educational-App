from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models import F
from django.db import transaction

# this class is for overriding default users manager of django user model
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise VlaueError('User must have a username')

        user = self.model(
                        email=self.normalize_email(email),
                        username=username,
                        is_staff=is_staff,
                        is_superuser=is_superuser
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
            is_superuser = True
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

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # resize profile image before saving
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)


class Student(User):

    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    ACADEMIC_YEAR = [
        ('FIRST', 1),
        ('SECOND', 2),
        ('THIRD', 3),
        ('FOURTH', 4),
        ('FIFTH', 5),
        ('SIXTH', 6),
        ('SEVENTH', 7),
    ]
    major = models.CharField(max_length=40)
    academic_year = models.IntegerField(blank=True, choices=ACADEMIC_YEAR)
    year_in_school = models.CharField(max_length=20, blank=True, choices=YEAR_IN_SCHOOL_CHOICES)
