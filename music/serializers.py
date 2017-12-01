from rest_framework import serializers
from .models import Song
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('user', 'title', 'artist', 'album')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
