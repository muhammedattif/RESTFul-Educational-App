from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import PlaylistSerializer, FavoriteSerializer
from playlists.models import Playlist, Favorite
from courses.api.serializers import ContentSerializer
from courses.models import Content
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
            content = Playlist.objects.get(id=playlist_id, owner=request.user).content.all()
            content = self.paginate_queryset(content, request, view=self)
            serializer = ContentSerializer(content, many=True)
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
        content, found, error = self.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        access_granted = self.allowed_to_access_content(request, content)
        if access_granted:
            playlist, found, error = self.get_playlist(request, playlist_id)
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            playlist.add(content)
            serializer = PlaylistSerializer(playlist, many=False)
            return Response(serializer.data)

        response = {
        'status': 'error',
        'message': 'Access denied!',
        'error_description': 'You don\'t have access to this resourse!, enroll this course to see its content.'
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, playlist_id, content_id, format=None):
        playlist, found, error = self.get_playlist(request, playlist_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        content, found, error = self.get_content(content_id)
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

    def get_content(self, content_id):
        try:
            return Content.objects.get(id=content_id), True, None
        except Content.DoesNotExist:
            error = {
            'status': 'error',
            'error_description': 'This content cannot be found'
            }
            return None, False, error

    def allowed_to_access_content(self, request, content):
        if content.can_access(request.user) or content.course.can_access(request.user):
            return content, True
        return None, False

class FavoriteList(APIView, PageNumberPagination):
    """
    List all content of favorites
    """

    def get(self, request, format=None):
        Favorites = Favorite.objects.filter(owner=request.user)
        Favorites = self.paginate_queryset(Favorites, request, view=self)
        serializer = FavoriteSerializer(Favorites, many=True)
        return Response(serializer.data)


class FavoriteContent(APIView):
    """
    Add or delete content from favorite
    """

    def put(self, request, content_id, format=None):
        content, found, error = self.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        access_granted = self.allowed_to_access_content(request, content)
        if access_granted:
            favorites = self.get_favorite_playlist(request)
            favorites.add(content)
            serializer = FavoriteSerializer(favorites, many=False)
            return Response(serializer.data)

        response = {
        'status': 'error',
        'message': 'Access denied!',
        'error_description': 'You don\'t have access to this resourse!, enroll this course to see its content.'
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, content_id, format=None):
        content, found, error = self.get_content(content_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        favorites = self.get_favorite_playlist(request)
        favorites.remove(content)
        serializer = FavoriteSerializer(favorites, many=False)
        return Response(serializer.data)


    def get_favorite_playlist(self, request):
        favorites, created =  Favorite.objects.get_or_create(owner=request.user)
        return favorites

    def get_content(self, content_id):
        try:
            return Content.objects.get(id=content_id), True, None
        except Content.DoesNotExist:
            error = {
            'status': 'error',
            'error_description': 'This content cannot be found'
            }
            return None, False, error

    def allowed_to_access_content(self, request, content):
        if content.can_access(request.user) or content.course.can_access(request.user):
            return content, True
        return None, False
