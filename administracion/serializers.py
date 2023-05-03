from rest_framework import serializers
from .models import Artist
from django.contrib.auth.models import User


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'realName', 'birthDate', 'info')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')