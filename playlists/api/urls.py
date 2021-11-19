from django.urls import path, include
from .views import get_all_playlists, get_playlist, playlist_contents, get_all_favorites, favorites_contents

app_name = 'playlists'

urlpatterns = [
  # Playlists APIs routes
  path('', get_all_playlists, name='playlists'),
  path('<int:playlist_id>', get_playlist, name='playlist'),
  path('<int:playlist_id>/contents/<int:content_id>/', playlist_contents, name='playlist_contents'),

  # Favorites APIs routes
  path('favorites/', get_all_favorites, name='favorites'),
  path('favorites/<int:content_id>/', favorites_contents, name='favorites_contents'),

]
