from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction

def atomic_post_save(sender, instance, **kwargs):
    if hasattr(instance, "atomic_post_save") and transaction.get_connection().in_atomic_block:
        transaction.on_commit(lambda: instance.atomic_post_save(sender, instance=instance, **kwargs))

post_save.connect(atomic_post_save)
