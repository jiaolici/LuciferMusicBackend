from rest_framework import serializers
from LuciferMusic.models import UserProfile,Artist,Song,Album

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','avatar','introduction','gender','birthday','city']

class ArtistRoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name']

class AlbumRoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id','name']

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistRoughSerializer(many=True,read_only=True)
    album = AlbumRoughSerializer(read_only=True)
    class Meta:
        model = Song
        fields = "__all__"

class AlbumSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Album
        fields = "__all__"

class ArtistSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    songs = SongSerializer(many=True, read_only=True)
    albums = AlbumSerializer(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = "__all__"

