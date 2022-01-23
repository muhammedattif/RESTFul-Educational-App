from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Teacher
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

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




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    title = "Reset your {title} account password".format(title="Emtyaz Advisor")
    email_plaintext_message = f"""
    Dear {reset_password_token.user.username},

    This is a secret key to reset your password: {reset_password_token.key}

    If you did not make the request, please ignore this message and your password will remain unchanged.
    """
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Emtyaz Advisor"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
