from .models import Artist, Event, EventArtist, Song, PlayList, PlayListSong
from rest_framework import viewsets
from .serializers import ArtistSerializer, UserSerializer, EventSerializer, SongSerializer, PlayListSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAdminUser



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]
    


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Obtener la lista de artistas seleccionados
        artist_ids = serializer.validated_data.pop('artist_ids', None)

        # Actualizar la información del evento
        self.perform_update(serializer)
        
        # Actualizar la relación event_artist del evento
        if artist_ids is not None:
            EventArtist.objects.filter(event=instance).delete() # Eliminar todos los artistas actuales
            for artist_id in artist_ids:
                artist = Artist.objects.get(id=artist_id)
                EventArtist.objects.create(artist=artist, event=instance)

        return Response(serializer.data)

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Obtener la lista de canciones seleccionadas
        song_ids = serializer.validated_data.pop('song_ids', None)

        # Actualizar la información de la playlist
        self.perform_update(serializer)
        
        # Actualizar la relación playlist_song de la playlist
        if song_ids is not None:
            PlayListSong.objects.filter(playList=instance).delete() # Eliminar todas las canciones actuales
            for song_id in song_ids:
                song = Song.objects.get(id=song_id)
                PlayListSong.objects.create(song=song, playList=instance)

        return Response(serializer.data)