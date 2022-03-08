from django.db import models
from django.conf import settings
from courses.models import Lecture

UserModel = settings.AUTH_USER_MODEL

class Favorite(models.Model):
    owner = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="favorites")
    lecture = models.ManyToManyField(Lecture, blank=True)

    def __str__(self):
          return self.owner.email

    def add(self, lecture):
        self.lectures.add(lecture)

    def remove(self, lecture):
        self.lectures.remove(lecture)

# Playlist Model
class Playlist(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="Playlists")
    name = models.CharField(max_length=20, unique=True)
    lecture = models.ManyToManyField(Lecture, blank=True)

    class Meta:
        unique_together = (("owner", "name"),)

    def __str__(self):
          return f'{self.owner.email}-{self.name}'

    def add(self, lecture):
        self.lectures.add(lecture)

    def remove(self, lecture):
        self.lectures.remove(lecture)

# Watch History
class WatchHistory(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="watch_history")
    lectures = models.ManyToManyField(Lecture, blank=True)

    class Meta:
        verbose_name_plural = 'Watch history'

    def __str__(self):
          return f'{self.user.email}-Watch History'

    def add_lecture(self, lecture):
        self.lectures.add(lecture)
        self.save()
