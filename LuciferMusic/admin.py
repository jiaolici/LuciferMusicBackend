from django.contrib import admin
from .models import UserProfile,Style,Artist,Album,Song,SongList,Fav

# Register your models here.
admin.site.register([UserProfile,Style,Artist,Album,Song,SongList,Fav])