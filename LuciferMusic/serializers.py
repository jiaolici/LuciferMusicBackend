from rest_framework import serializers
from LuciferMusic.models import UserProfile,Artist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','avatar','introduction','gender','birthday','city']

class ArtistSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Artist
        fields = "__all__"