from rest_framework import serializers
from .models import Artist, Event, EventArtist
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
    event_artist = EventArtistSerializer(many=True, source='eventartist_set')

    class Meta:
        model = Event
        fields = ('id', 'name', 'place', 'date', 'event_artist')