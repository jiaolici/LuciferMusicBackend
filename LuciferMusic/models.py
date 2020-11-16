from django.db import models

# Create your models here.
# django 2.2.3
# restframework 3.10.1
# jwt 1.11.0
# python 3.7.4
# django-cors-headers 3.3.0
# apscheduler 3.6.3
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

# 扩展User类
class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to="user_avatar")
    introduction = models.CharField(max_length=100)
    gender = models.CharField(max_length=2,choices=(("男","男"),("女","女")))
    birthday = models.DateField(default="2019-1-1")
    city = models.CharField(max_length=10)
    class Meta(AbstractUser.Meta):
        pass


class Fav(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    fav_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user','content_type','object_id')

class Style(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name


class ListenRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # times = models.PositiveIntegerField(default=0)
    # update_time = models.DateTimeField(auto_now=True)
    time = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # class Meta:
    #     unique_together = ('user','content_type','object_id')

class Artist(models.Model):
    name = models.CharField(max_length=100,unique=True)
    alias = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to = "artist_avatar")
    styles = models.ManyToManyField(Style)
    introduction = models.TextField()
    country = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name="albums")
    cover = models.ImageField(upload_to="album_cover")
    styles = models.ManyToManyField(Style)
    company = models.CharField(max_length=20)
    publish_date = models.DateField()
    introduction = models.TextField()
    favs = GenericRelation(Fav)
    listen_records = GenericRelation(ListenRecord)
    class Meta:
        unique_together = ('name','artist')

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist,related_name='songs')
    audio = models.FileField(upload_to="audio")
    lyric = models.TextField()
    duration = models.PositiveIntegerField()
    album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name="songs")
    listen_records = GenericRelation(ListenRecord)

    class Meta:
        unique_together = ('name','album')

    def __str__(self):
        return self.name

class SongList(models.Model):
    name = models.CharField(max_length=100)
    styles = models.ManyToManyField(Style)
    cover = models.ImageField(upload_to="songlist_cover",null=True)
    creator = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add = True)
    songs = models.ManyToManyField(Song)
    favs = GenericRelation(Fav)
    listen_records = GenericRelation(ListenRecord)
    class Meta:
        unique_together = ('name','creator')
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    replay_target = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Praise(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    click_time = models.DateTimeField(auto_now_add=True)
    # 点赞对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user','content_type','object_id')

class Rank(models.Model):
    name = models.CharField(max_length=100,default="榜单")
    cover = models.ImageField(upload_to="rank_cover")
    introduction = models.TextField(default="introduction")
    cron_str = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    rule = models.CharField(max_length=100)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name

class RankSongs(models.Model):
    rank = models.ForeignKey(Rank,on_delete=models.CASCADE,related_name="rank_songs")
    songs = models.ManyToManyField(Song)
    from_date = models.DateTimeField(null=False)
    update_at = models.DateTimeField(auto_now_add=True)
