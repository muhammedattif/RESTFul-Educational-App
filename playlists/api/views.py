from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlaylistSerializer, FavoriteSerializer
from playlists.models import Playlist, Favorite
from courses.models import Content
from rest_framework import status


@api_view(['GET'])
def get_all_playlists(request):
    playlists = Playlist.objects.prefetch_related('content').filter(owner=request.user)
    serializer = PlaylistSerializer(playlists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_playlist(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    serializer = PlaylistSerializer(playlist, many=False)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def playlist_contents(request, playlist_id, content_id):
    content = Content.objects.get(id=content_id)
    if content.can_access(request.user) or content.course.can_access(request.user):
        playlist, created = Playlist.objects.get_or_create(id=playlist_id, owner=request.user)
        if request.method == 'PUT':
            playlist.add(content)
        else:
            playlist.remove(content)
        serializer = PlaylistSerializer(playlist, many=False)
        return Response(serializer.data)

    response = {
    'status': 'error',
    'message': 'Access denied!',
    'error_description': 'You don\'t have access to this resourse!, enroll this course to see its content.'
    }
    return Response(response, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def get_all_favorites(request):
    Favorites = Favorite.objects.filter(owner=request.user)
    serializer = FavoriteSerializer(Favorites, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def favorites_contents(request, content_id):
    content = Content.objects.get(id=content_id)
    if content.can_access(request.user) or content.course.can_access(request.user):
        favorites, created = Favorite.objects.get_or_create(owner=request.user)
        if request.method == 'PUT':
            favorites.add(content)
        else:
            favorites.remove(content)
        serializer = FavoriteSerializer(favorites, many=False)
        return Response(serializer.data)

    response = {
    'status': 'error',
    'message': 'Access denied!',
    'error_description': 'You don\'t have access to this resourse!, enroll this course to see its content.'
    }
    return Response(response, status=status.HTTP_403_FORBIDDEN)
