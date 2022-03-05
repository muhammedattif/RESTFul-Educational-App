from django.db import models

class Category(models.Model):

    # add initial values to db when migrating

    name = models.CharField(max_length=40, unique=True)
    icon = models.FileField(upload_to='categories/icons')
    title = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
