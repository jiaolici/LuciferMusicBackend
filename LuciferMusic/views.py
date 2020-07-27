from django.shortcuts import render
from .models import UserProfile,Artist
from .serializers import UserSerializer,ArtistSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
class UserViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class ArtistViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()