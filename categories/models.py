from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=40)
    icon = models.FileField(upload_to='categories/icons')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
