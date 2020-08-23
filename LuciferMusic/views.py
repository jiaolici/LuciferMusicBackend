from django.shortcuts import render
from .models import UserProfile,Artist,Album,Song,SongList,Fav
from .serializers import UserSerializer,ArtistSerializer,AlbumSerializer,SongSerializer,SongListSerializer,FavSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class UserViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class ArtistViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

class AlbumViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

class SongViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

class SongListViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = SongListSerializer
    queryset = SongList.objects.all()

class FavViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin):
    serializer_class = FavSerializer
    queryset = Fav.objects.all()

    def create(self, request, *args, **kwargs):
        if(request.data['content_type'] == "album"):
            content_type = ContentType.objects.get_for_model(Album)
        elif(request.data['content_type'] == "songlist"):
            content_type = ContentType.objects.get_for_model(SongList)
        else:
            return Response({"error":"no such content_type"},status=status.HTTP_400_BAD_REQUEST)
        request.data['content_type'] = content_type.id
        return super().create(request)