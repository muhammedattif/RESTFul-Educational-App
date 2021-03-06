from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction
from .models import QuizAttempt, QuizResult, Lecture
from moviepy.editor import VideoFileClip, AudioFileClip


def atomic_post_save(sender, instance, **kwargs):
    if hasattr(instance, "atomic_post_save") and transaction.get_connection().in_atomic_block:
        transaction.on_commit(lambda: instance.atomic_post_save(sender, instance=instance, **kwargs))

post_save.connect(atomic_post_save)


@receiver(post_save, sender=QuizResult)
def add_quiz_attempt(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.question == instance.quiz.questions.last():
            QuizAttempt.objects.create(user=instance.user, quiz=instance.quiz)

# @receiver(post_save, sender=Lecture)
# def calculate_duration(sender, instance=None, created=False, **kwargs):
#     if created:
#         if instance.video:
#             video = VideoFileClip(instance.video.path)
#             instance.duration = video.duration # this will return the length of the video in seconds
#             instance.save()
#     else:
#         if instance.video:
#             video = VideoFileClip(instance.video.path)
#             instance.duration = video.duration # this will return the length of the video in seconds
#             instance.save()
