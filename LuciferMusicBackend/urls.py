"""LuciferMusicBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from LuciferMusic.views import UserViewset,ArtistViewset,AlbumViewset,SongViewset,SongListViewset,FavViewset,CommentViewset,PraiseViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token
from LuciferMusicBackend.settings import MEDIA_ROOT

router = DefaultRouter()
router.register(r'user', UserViewset, basename="user")
router.register(r'artist', ArtistViewset, basename="artist")
router.register(r'album', AlbumViewset, basename="album")
router.register(r'song', SongViewset, basename="song")
router.register(r'songlist', SongListViewset, basename="songlist")
router.register(r'fav', FavViewset, basename="fav")
router.register(r'comment', CommentViewset, basename="comment")
router.register(r'praise', PraiseViewset, basename="praise")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token ),
    path('refresh/', refresh_jwt_token ),
    path('verify/', verify_jwt_token ),
    path('api-token-auth/', views.obtain_auth_token),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    re_path('^', include(router.urls))
]
