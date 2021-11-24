from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import PlaylistSerializer, FavoriteSerializer, WatchHistorySerializer
from playlists.models import Playlist, Favorite, WatchHistory
from courses.api.serializers import FullContentSerializer
from courses.models import Content
import courses.utils as utils
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class PlaylistList(APIView, PageNumberPagination):
    """
    List all playlists, or create a new playlist.
    """

    def get(self, request, format=None):
        playlists = Playlist.objects.prefetch_related('content').filter(owner=request.user)
        playlists = self.paginate_queryset(playlists, request, view=self)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        return self.create(request)

    def create(self, request):
        playlist_data = request.data
        playlist_data['owner'] = request.user.id
        serializer = PlaylistSerializer(data=playlist_data)
        if serializer.is_valid():
            serializer.save()
            response = {
            'status': 'success',
            'message': 'Playlist created successfully!',
            'playlist_data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
        'status': 'error',
        'message': 'Playlist with this name already exists.',
        'error_description': serializer.errors
        }
        return Response(response, status=status.HTTP_409_CONFLICT)


class PlaylistDetail(APIView, PageNumberPagination):
    """
    List all playlist's details.
    """

    def get(self, request, playlist_id, format=None):
        try:
            content = Playlist.objects.get(id=playlist_id, owner=request.user).content.prefetch_related('privacy__shared_with')
            content = self.paginate_queryset(content, request, view=self)
            serializer = FullContentSerializer(content, many=True)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            response = {
            'status': 'error',
            'message': 'Playlist is not found!',
            'error_description': 'You don\'t have any playlist with this name.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class PlaylistContent(APIView):
    """
    Add or remove content from a playlist
    """

    def put(self, request, playlist_id, content_id, format=None):
        content, found, error = utils.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            playlist, found, error = self.get_playlist(request, playlist_id)
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            playlist.add(content)
            serializer = PlaylistSerializer(playlist, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, playlist_id, content_id, format=None):
        playlist, found, error = self.get_playlist(request, playlist_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        content, found, error = utils.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        playlist.remove(content)
        serializer = PlaylistSerializer(playlist, many=False)
        return Response(serializer.data)

    def get_playlist(self, request, playlist_id):
        try:
            return Playlist.objects.get(id=playlist_id, owner=request.user), True, None
        except Playlist.DoesNotExist:
            error = {
            'status': 'error',
            'error_description': 'Playlist is not found.'
            }
            return None, False, error


class FavoriteList(APIView, PageNumberPagination):
    """
    List all content of favorites
    """

    def get(self, request, format=None):
        Favorites = Favorite.objects.get(owner=request.user).content.prefetch_related('privacy__shared_with')
        Favorites = self.paginate_queryset(Favorites, request, view=self)
        serializer = FullContentSerializer(Favorites, many=True)
        return Response(serializer.data)


class FavoriteContent(APIView):
    """
    Add or delete content from favorite
    """

    def put(self, request, content_id, format=None):
        content, found, error = utils.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        access_granted = utils.allowed_to_access_content(request.user, content)
        if access_granted:
            favorites = self.get_favorite_playlist(request)
            favorites.add(content)
            serializer = FavoriteSerializer(favorites, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, content_id, format=None):
        content, found, error = utils.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        favorites = self.get_favorite_playlist(request)
        favorites.remove(content)
        serializer = FavoriteSerializer(favorites, many=False)
        return Response(serializer.data)


    def get_favorite_playlist(self, request):
        favorites, created =  Favorite.objects.get_or_create(owner=request.user)
        return favorites


class WatchHistoryList(APIView, PageNumberPagination):

    def get(self, request, format=None):
        user_watch_history, created = WatchHistory.objects.get_or_create(user=request.user)
        user_watch_history_contents = user_watch_history.contents.all()
        user_watch_history_contents = self.paginate_queryset(user_watch_history_contents, request, view=self)
        serializer = FullContentSerializer(user_watch_history_contents, many=True)
        return Response(serializer.data)