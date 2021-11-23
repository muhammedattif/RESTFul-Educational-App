from django.db import models
from courses.models import Course
from model_utils import Choices
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

class CourseEnrollment(models.Model):

    PAYMENT_METHODS = Choices(
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    PAYMENT_TYPES = Choices(
        ('telegram', 'Telegram'),
        ('fawry', 'Fawry'),
        ('visa', 'Visa'),
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='courses_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default=PAYMENT_METHODS.offline)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default=PAYMENT_TYPES.telegram)
    date_created = models.DateTimeField(auto_now_add=True)
