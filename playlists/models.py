from django.db import models
from django.conf import settings
from courses.models import Content

UserModel = settings.AUTH_USER_MODEL

class Favorite(models.Model):
    owner = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="favorites")
    content = models.ManyToManyField(Content, blank=True)

    def __str__(self):
          return self.owner.email

    def add(self, content):
        self.content.add(content)

    def remove(self, content):
        self.content.remove(content)

# Playlist Model
class Playlist(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="Playlists")
    name = models.CharField(max_length=20, unique=True)
    content = models.ManyToManyField(Content, blank=True)

    class Meta:
        unique_together = (("owner", "name"),)

    def __str__(self):
          return f'{self.owner.email}-{self.name}'

    def add(self, content):
        self.content.add(content)

    def remove(self, content):
        self.content.remove(content)

# Watch History
class WatchHistory(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="watch_history")
    contents = models.ManyToManyField(Content, blank=True)

    class Meta:
        verbose_name_plural = 'Watch history'

    def __str__(self):
          return f'{self.user.email}-Watch History'

    def add_content(self, content):
        self.contents.add(content)
        self.save()
