from django.urls import path, include
from .views import FavoriteController, PlaylistList, PlaylistLecture, WatchHistoryList

app_name = 'playlists'

urlpatterns = [
  # Playlists APIs routes
  # path('', get_all_playlists, name='playlists'),
  path('', PlaylistList.as_view()),
  path('<int:playlist_id>', PlaylistLecture.as_view(), name='playlist_lectures'),

  # Favorites APIs routes
  path('favorites', FavoriteController.as_view(), name='favorites'),

  # History APIs
  path('watch_history/', WatchHistoryList.as_view(), name='watch_history'),

]
