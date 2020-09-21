from django.shortcuts import render
from .models import UserProfile,Artist,Album,Song,SongList,Fav,Comment,Praise
from .serializers import UserSerializer,ArtistSerializer,AlbumSerializer,SongSerializer,SongListSerializer,FavSerializer,CommentSerializer,PraiseSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from .paginations import CommentPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class UserViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class ArtistViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

class AlbumViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request)
        res.data['is_fav'] = False
        print(request.user)
        if(not request.user.is_anonymous):
            content_type = ContentType.objects.get_for_model(Album)
            try:
                fav_obj = Fav.objects.get(content_type=content_type,object_id=res.data['id'],user=request.user)
                res.data['is_fav'] = True
                res.data['fav_id'] = fav_obj.id
            except Fav.DoesNotExist:
                pass
        return res

class SongViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

class SongListViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = SongListSerializer
    queryset = SongList.objects.all()

class FavViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin):
    serializer_class = FavSerializer
    queryset = Fav.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if(request.data['content_type'] == "album"):
            content_type = ContentType.objects.get_for_model(Album)
        elif(request.data['content_type'] == "songlist"):
            content_type = ContentType.objects.get_for_model(SongList)
        else:
            return Response({"error":"no such content_type"},status=status.HTTP_400_BAD_REQUEST)
        request.data['content_type'] = content_type.id
        return super().create(request)

class CommentViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin):
    serializer_class = CommentSerializer
    # queryset = Comment.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.all()
        target_type = self.request.query_params.get('type', None)
        target_object_id = self.request.query_params.get('target_id', None)
        target_content_type = None
        if(target_type=='album'):
            target_content_type = ContentType.objects.get_for_model(Album)
        if(target_content_type and target_object_id):
            queryset = queryset.filter(content_type=target_content_type.id,object_id=target_object_id)
        return queryset

    def create(self, request, *args, **kwargs):
        if(request.data['content_type'] == "album"):
            content_type = ContentType.objects.get_for_model(Album)
        elif(request.data['content_type'] == "songlist"):
            content_type = ContentType.objects.get_for_model(SongList)
        else:
            return Response({"error":"no such content_type"},status=status.HTTP_400_BAD_REQUEST)
        request.data['content_type'] = content_type.id
        return super().create(request)
    
    def perform_create(self,serializer):
        user_id = self.request.data['user_id']
        replay_target_id = self.request.data.get('replay_target_id',None)
        serializer.save(user_id = user_id,replay_target_id = replay_target_id)

    def list(self, request, *args, **kwargs):
        res = super().list(request)
        content_type = ContentType.objects.get_for_model(Comment)
        for comment in res.data.get('results',[]):
            praises = Praise.objects.filter(content_type=content_type, object_id=comment.get('id',None))
            comment['pra_count'] = len(praises)
            if(len(praises)<=0):
                continue
            if (not request.user.is_anonymous):
                try:
                    pra_obj = praises.get(content_type=content_type, object_id=comment.get('id',None), user=request.user)
                    comment['is_praised'] = True
                    comment['praise_id'] = pra_obj.id
                except Praise.DoesNotExist:
                    pass
        return res

class PraiseViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin):
    serializer_class = PraiseSerializer
    queryset = Praise.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)