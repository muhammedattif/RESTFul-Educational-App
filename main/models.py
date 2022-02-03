from django.db import models


class ContactUs(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    telegram_username = models.CharField(max_length=100)
    messenger_username = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.email
