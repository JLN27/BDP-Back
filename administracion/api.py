from .models import Artist, Event, EventArtist, Song, PlayList
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
from rest_framework import permissions
from rest_framework.permissions import BasePermission


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
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
            user = self.request.user
            if user.groups.filter(name='editors').exists():
                permission_classes.append(DenyAll)
        return [permission() for permission in permission_classes]

class DenyAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
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
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        artist_id = request.data.get('artist_id')
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return Response({'artist_id': f'Artist with id {artist_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(artist=artist)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.created_by == request.user

class ReadOnlyUnlessCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.created_by == request.user

class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Obtener la instancia del usuario que está creando la playlist
        user = request.user

        # Establecer el usuario que realizó la solicitud como el creador de la lista de reproducción
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
            # Eliminar todas las canciones actuales
            instance.songs.clear()
            
            # Agregar las nuevas canciones a la playlist
            for song_id in song_ids:
                song = Song.objects.get(id=song_id)
                instance.songs.add(song)

        return Response(serializer.data)


