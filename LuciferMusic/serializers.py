from rest_framework import serializers
from LuciferMusic.models import UserProfile,Artist,Song,Album,SongList,Fav,Comment,Praise,ListenRecord,Rank,RankSongs
from rest_framework.fields import empty
from django.db import models

class UserRoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','avatar']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','avatar','introduction','gender','birthday','city']

class ArtistRoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name']

class AlbumRoughSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Album
        fields = ['id','name','cover','publish_date','styles']

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistRoughSerializer(many=True,read_only=True)
    album = AlbumRoughSerializer(read_only=True)
    class Meta:
        model = Song
        fields = "__all__"

class AlbumSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    artist = ArtistRoughSerializer(read_only=True)
    songs = SongSerializer(many=True, read_only=True)
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

class SongListSerializer(serializers.ModelSerializer):
    styles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    songs = SongSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)
    class Meta:
        model = SongList
        fields = "__all__"

class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fav
        fields = "__all__"

class CommentRoughSerializer(serializers.ModelSerializer):
    user = UserRoughSerializer(read_only=False)
    class Meta:
        model = Comment
        fields = ['id','content','user']

class CommentSerializer(serializers.ModelSerializer):
    replay_target = CommentRoughSerializer(read_only=True)
    user = UserRoughSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

class PraiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Praise
        fields = "__all__"

class ListenRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListenRecord
        fields = "__all__"


class RankSongsSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = RankSongs
        fields = "__all__"

class RankSerializer(serializers.ModelSerializer):
    # rank_songs = RankSongsSerializer(many=True, read_only=True)
    rank_songs = serializers.SerializerMethodField()

    # obj是一个Rank对象
    def get_rank_songs(self, obj):
        qs = RankSongs.objects.filter(rank__id=obj.id).order_by("-update_at")
        if qs.count()>0:
            # 加入_context
            return RankSongsSerializer(qs[0],context=self._context).data
        return {}


    class Meta:
        model = Rank
        fields = "__all__"