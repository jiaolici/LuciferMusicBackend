from django.db import models

# Create your models here.
# django 2.2.3
# restframework 3.10.1
# jwt 1.11.0
# python 3.7.4
# django-cors-headers
from django.contrib.auth.models import AbstractUser
from django.db import models

# 扩展User类
class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to="user_avatar")
    introduction = models.CharField(max_length=100)
    gender = models.CharField(max_length=2,choices=(("男","男"),("女","女")))
    birthday = models.DateField(default="2019-1-1")
    city = models.CharField(max_length=10)
    class Meta(AbstractUser.Meta):
        pass

class Style(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

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

    class Meta:
        unique_together = ('name','album')

    def __str__(self):
        return self.name

class SongList(models.Model):
    name = models.CharField(max_length=100)
    styles = models.ManyToManyField(Style)
    cover = models.ImageField(upload_to="songlist_cover")
    creator = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add = True)
    songs = models.ManyToManyField(Song)
    class Meta:
        unique_together = ('name','creator')
    
    def __str__(self):
        return self.name