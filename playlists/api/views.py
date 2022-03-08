from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import PlaylistSerializer, FavoriteSerializer, WatchHistorySerializer
from playlists.models import Playlist, Favorite, WatchHistory
from courses.api.serializers import FullLectureSerializer
from courses.models import Lecture
import courses.utils as utils
import alteby.utils as general_utils
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class PlaylistList(APIView, PageNumberPagination):
    """
    List all playlists, or create a new playlist.
    """

    def get(self, request, format=None):
        playlists = Playlist.objects.prefetch_related('lectures').filter(owner=request.user)
        playlists = self.paginate_queryset(playlists, request, view=self)
        serializer = PlaylistSerializer(playlists, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        return self.create(request)

    def create(self, request):
        playlist_data = request.data
        playlist_data['owner'] = request.user.id
        serializer = PlaylistSerializer(data=playlist_data, context={'request': request})
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


class PlaylistLecture(APIView):

    """
    List all playlist's details.
    """

    def get(self, request, playlist_id, format=None):
        try:
            lectures = Playlist.objects.get(id=playlist_id, owner=request.user).lectures.prefetch_related('privacy__shared_with')
            lectures = self.paginate_queryset(lectures, request, view=self)
            serializer = FullLectureSerializer(lectures, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        except Playlist.DoesNotExist:
            response = {
            'status': 'error',
            'message': 'Playlist is not found!',
            'error_description': 'You don\'t have any playlist with this name.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    """
    Add or remove lecture from a playlist
    """

    def put(self, request, playlist_id, format=None):

        try:
            request_body = request.data
            lecture_id = request_body['lecture_id']
        except Exception as e:
            return Response(general_utils.error('required_fields'), status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs = {
        'id': lecture_id
        }
        lecture, found, error = utils.get_object(model=Lecture, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_lecture(request.user, lecture):
            playlist, found, error = self.get_playlist(request, playlist_id)
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            playlist.add(lecture)
            serializer = PlaylistSerializer(playlist, many=False, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, playlist_id, lecture_id, format=None):
        playlist, found, error = self.get_playlist(request, playlist_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        filter_kwargs = {
        'id': lecture_id
        }
        lecture, found, error = utils.get_object(model=Lecture, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        playlist.remove(lecture)
        serializer = PlaylistSerializer(playlist, many=False, context={'request': request})
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



class FavoriteController(APIView):

    """
    List all lecture of favorites
    """

    def get(self, request, format=None):
        favorites, created = Favorite.objects.get_or_create(owner=request.user)
        lectures = favorites.lectures.prefetch_related('privacy__shared_with')
        lectures = self.paginate_queryset(lectures, request, view=self)
        serializer = FullLectureSerializer(lectures, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


    """
    Add or delete lecture from favorite
    """

    def put(self, request, format=None):
        try:
            request_body = request.data
            lecture_id = request_body['lecture_id']
        except Exception as e:
            return Response(general_utils.error('required_fields'), status=status.HTTP_400_BAD_REQUEST)


        filter_kwargs = {
        'id': lecture_id
        }
        lecture, found, error = utils.get_object(model=Lecture, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        access_granted = utils.allowed_to_access_lecture(request.user, lecture)
        if access_granted:
            favorites = self.get_favorite_playlist(request)
            favorites.add(lecture)
            serializer = FavoriteSerializer(favorites, many=False, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, lecture_id, format=None):

        filter_kwargs = {
        'id': lecture_id
        }
        lecture, found, error = utils.get_object(model=Lecture, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        favorites = self.get_favorite_playlist(request)
        favorites.remove(lecture)
        serializer = FavoriteSerializer(favorites, many=False, context={'request': request})
        return Response(serializer.data)


    def get_favorite_playlist(self, request):
        favorites, created =  Favorite.objects.get_or_create(owner=request.user)
        return favorites


class WatchHistoryList(APIView, PageNumberPagination):

    def get(self, request, format=None):
        user_watch_history, created = WatchHistory.objects.get_or_create(user=request.user)
        user_watch_history_lectures = user_watch_history.lectures.prefetch_related('privacy__shared_with')
        user_watch_history_lectures = self.paginate_queryset(user_watch_history_lectures, request, view=self)
        serializer = FullLectureSerializer(user_watch_history_lectures, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
