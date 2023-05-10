from rest_framework import serializers
from .models import Artist, Event, EventArtist, Song, PlayList, PlayListSong
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
    

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'realName', 'birthDate', 'info')
   

class EventArtistSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = EventArtist
        fields = ('artist',)


class EventSerializer(serializers.ModelSerializer):
    artists = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'place', 'date', 'artists']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['artists'] = ArtistSerializer(instance.artists.all(), many=True).data
        return rep

    def to_internal_value(self, data):
        artist_ids = data.get('artist_ids', [])
        artists = []
        for artist_id in artist_ids:
            try:
                artist = Artist.objects.get(id=artist_id)
                artists.append(artist.pk)
            except Artist.DoesNotExist:
                # Si un id de artista no existe, puedes lanzar una excepción personalizada o simplemente continuar sin hacer nada
                pass

        data['artists'] = artists
        return super().to_internal_value(data)
    
   
class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), source='artist', write_only=True)

    class Meta:
        model = Song
        fields = ('id', 'title', 'image', 'audio', 'video', 'artist', 'artist_id')

    def create(self, validated_data):
        artist_id = validated_data.pop('artist', None)
        artist = None
        if artist_id:
            artist = Artist.objects.get(pk=artist_id.id)
        song = Song.objects.create(artist=artist, **validated_data)
        return song





class PlayListSongSerializer(serializers.ModelSerializer):
    song = SongSerializer()

    class Meta:
        model = PlayListSong
        fields = ('song',)


class PlayListSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True)
    song_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'songs', 'song_ids', 'created_by')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['songs'] = SongSerializer(instance.songs.all(), many=True).data
        return rep
