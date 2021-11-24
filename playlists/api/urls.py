from django.urls import path, include
from .views import FavoriteList, FavoriteContent, PlaylistList, PlaylistDetail, PlaylistContent, WatchHistoryList

app_name = 'playlists'

urlpatterns = [
  # Playlists APIs routes
  # path('', get_all_playlists, name='playlists'),
  path('', PlaylistList.as_view()),
  path('<int:playlist_id>', PlaylistDetail.as_view(), name='playlist'),
  path('<int:playlist_id>/contents/<int:content_id>/', PlaylistContent.as_view(), name='playlist_content'),

  # Favorites APIs routes
  path('favorites/', FavoriteList.as_view(), name='favorites'),
  path('favorites/<int:content_id>/', FavoriteContent.as_view(), name='favorites_contents'),

  # History APIs
  path('watch_history/', WatchHistoryList.as_view(), name='watch_history'),

]
