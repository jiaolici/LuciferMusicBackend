from django.shortcuts import render
from .models import UserProfile,Artist,Album,Song,SongList,Fav,Comment,Praise,ListenRecord,Rank
from .serializers import UserSerializer,ArtistSerializer,AlbumSerializer,SongSerializer,SongListSerializer,FavSerializer,CommentSerializer,PraiseSerializer,ListenRecordSerializer,RankSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from .paginations import CommentPagination,SongPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import generics
from django.db.models import Count,Max

# Create your views here.
class UserViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class ArtistViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

class AlbumViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        queryset = Album.objects.all()
        fav_user_id = self.request.query_params.get("fav_user_id", None)
        if (fav_user_id):
            content_type = ContentType.objects.get_for_model(Album)
            queryset = queryset.filter(favs__user__id=fav_user_id, favs__content_type=content_type)
        return queryset

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

class SongViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    pagination_class = SongPagination

    def get_queryset(self):
        queryset = Song.objects.all()
        user_id = self.request.query_params.get("user_id",None)
        if(not user_id):
            return queryset
        # queryset = queryset.filter(listen_records__user__id=user_id).order_by("-listen_records__times")
        queryset = queryset.filter(listen_records__user__id=user_id).annotate(Count('listen_records')).order_by("-listen_records__count")
        return queryset

    def list(self, request, *args, **kwargs):
        res = super().list(request)
        content_type = ContentType.objects.get_for_model(Song)
        for song in res.data.get('results', []):
            # record = ListenRecord.objects.get(content_type=content_type, object_id=song.get('id', None))
            # song['listen_times'] = record.times
            user_id = self.request.query_params.get("user_id", None)
            if (not user_id):
                song['listen_times'] = ListenRecord.objects.filter(content_type=content_type, object_id=song.get('id', None)).count()
            else:
                song['listen_times'] = ListenRecord.objects.filter(content_type=content_type, object_id=song.get('id', None),user__id=user_id).count()
        return res

class SongListViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    serializer_class = SongListSerializer
    queryset = SongList.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = SongList.objects.all()
        creator_id = self.request.query_params.get("creator_id",None)
        fav_user_id = self.request.query_params.get("fav_user_id", None)
        if(creator_id):
            queryset = queryset.filter(creator__id=creator_id)
        elif(fav_user_id):
            content_type = ContentType.objects.get_for_model(SongList)
            queryset = queryset.filter(favs__user__id=fav_user_id,favs__content_type=content_type)
        return queryset

    def perform_create(self,serializer):
        creator_id = self.request.data['creator_id']
        serializer.save(creator_id = creator_id)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request)
        res.data['is_fav'] = False
        if(not request.user.is_anonymous):
            content_type = ContentType.objects.get_for_model(SongList)
            try:
                fav_obj = Fav.objects.get(content_type=content_type,object_id=res.data['id'],user=request.user)
                res.data['is_fav'] = True
                res.data['fav_id'] = fav_obj.id
            except Fav.DoesNotExist:
                pass
        return res

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
        elif(target_type=='song'):
            target_content_type = ContentType.objects.get_for_model(Song)
        elif (target_type == 'songlist'):
            target_content_type = ContentType.objects.get_for_model(SongList)
        if(target_content_type and target_object_id):
            queryset = queryset.filter(content_type=target_content_type.id,object_id=target_object_id)
        return queryset

    def create(self, request, *args, **kwargs):
        if(request.data['content_type'] == "album"):
            content_type = ContentType.objects.get_for_model(Album)
        elif (request.data['content_type'] == "song"):
            content_type = ContentType.objects.get_for_model(Song)
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

    def create(self, request, *args, **kwargs):
        if(request.data['content_type'] == "comment"):
            content_type = ContentType.objects.get_for_model(Comment)
        else:
            return Response({"error":"no such content_type"},status=status.HTTP_400_BAD_REQUEST)
        request.data['content_type'] = content_type.id
        return super().create(request)

class ListenRecordViewset(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class = ListenRecordSerializer
    queryset = ListenRecord.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if(request.user.is_anonymous):
            return Response(data={"error":"Permission Denied"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data['content_type'] == "album"):
            content_type = ContentType.objects.get_for_model(Album)
        elif (request.data['content_type'] == "songlist"):
            content_type = ContentType.objects.get_for_model(SongList)
        elif (request.data['content_type'] == "song"):
            content_type = ContentType.objects.get_for_model(Song)
        else:
            return Response(data={"error": "No Such Content Type"}, status=status.HTTP_400_BAD_REQUEST)
        object_id = request.data.get('object_id', None)
        if not object_id:
            return Response(data={"error": "No Object ID"}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     obj = ListenRecord.objects.get(content_type=content_type,object_id=object_id,user=request.user)
        #     obj.times = obj.times + 1
        #     # print(obj.content_object)
        #     obj.save()
        # except ListenRecord.DoesNotExist:
        #     # obj = ListenRecord.objects.create(content_type=content_type,object_id=object_id,user=request.user,times=1)
        #     # print(obj.content_object)
        #     obj = ListenRecord(content_type=content_type,object_id=object_id,user=request.user,times=1)
        #     if(obj.content_object == None):
        #         return Response(data={"error": "object id not found"}, status=status.HTTP_400_BAD_REQUEST)
        #     obj.save()
        obj = ListenRecord(content_type=content_type, object_id=object_id, user=request.user)
        if (obj.content_object == None):
            return Response(data={"error": "object id not found"}, status=status.HTTP_400_BAD_REQUEST)
        obj.save()
        return Response(data={"res": "success"}, status=status.HTTP_200_OK)


class RankViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()


class SongListOp(APIView):
    def get_object(self, pk):
        try:
            return SongList.objects.get(pk=pk)
        except SongList.DoesNotExist:
            raise status.Http404
    def patch(self, request, pk, format=None):
        songList = self.get_object(pk)
        songIds = request.data.get("songIds",None)
        if(songIds):
            songs = Song.objects.filter(Q(id__in=songIds))
            songList.songs.add(*songs)
            songList.save()
        serializer = SongListSerializer(songList)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        songList = self.get_object(pk)
        songIds = request.data.get("songIds", None)
        if (songIds):
            songs = Song.objects.filter(Q(id__in=songIds))
            songList.songs.delete(*songs)
            songList.save()
        serializer = SongListSerializer(songList)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IndexSongList(generics.ListAPIView):
    serializer_class = SongListSerializer
    # queryset = SongList.objects.order_by("-listen_records__times")[0:6]
    queryset = SongList.objects.annotate(Count('listen_records')).order_by("-listen_records__count")[0:6]

class IndexAlbum(generics.ListAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.order_by("-publish_date")[0:4]

class IndexRank(generics.ListAPIView):
    serializer_class = RankSerializer
    queryset = Rank.objects.annotate(Max('rank_songs__update_at')).order_by("-rank_songs__update_at__max")[0:4]