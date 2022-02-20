from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user, body, target_object=None):
   action = Action(user=user, body=body, target_object=target_object)
   action.save()
