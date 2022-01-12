from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Teacher
from rest_framework.authtoken.models import Token
from django.conf import settings

UserModel = settings.AUTH_USER_MODEL

@receiver(post_save, sender=UserModel)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Student.objects.create(user=instance)
        if instance.is_teacher:
            Teacher.objects.create(user=instance)
