from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from .settings import actions_types

User = get_user_model()

class Action(models.Model):

    user = models.ForeignKey(
                            User,
                            db_index=True,
                            on_delete=models.CASCADE,
                            related_name='actions')
    action_type = models.CharField(max_length=255, choices=actions_types)
    body = models.CharField(max_length=255)
    target_model = models.ForeignKey(ContentType,
                                     blank=True,
                                     null=True,
                                     related_name='target_obj',
                                     on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target_object = GenericForeignKey('target_model', 'target_id')
    created_at = models.DateTimeField(auto_now_add=True,
                                  db_index=True)
    class Meta:
        ordering = ('-created_at',)
