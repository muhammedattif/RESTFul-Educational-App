from rest_framework import serializers
from playlists.models import Playlist, Favorite
from courses.api.serializers import ContentSerializer

class PlaylistSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True)
    class Meta:
        model = Playlist
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'
