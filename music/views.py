# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Song
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, View
from django.core.urlresolvers import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SongSerializer, UserSerializer
from rest_framework.parsers import JSONParser, MultiPartParser
import json


def get_song_variables(details, key):
    for x in details:
        if key in x:
            variable = details[x]

    return variable


def get_user_from_song(details):
    if details.get('user') is not None:
        user = [details.get('user')]
    else:
        user = []

    return user


# REST Api
# /songs
class SongList(APIView):

    serializer_class = SongSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        song_details = request.data

        artist = get_song_variables(song_details, "artist")
        album = get_song_variables(song_details, "album")
        title = get_song_variables(song_details, "title")
        user = get_user_from_song(song_details)

        serializer = SongSerializer(data={u'album': album, u'title': title, u'artist': artist, u'user': user})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /users
class UserList(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_songs(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        songs = Song.objects.filter(title__contains=q)
        results = []
        for song in songs:
            song_json = {}
            song_json['id'] = song.title
            song_json['label'] = song.title
            song_json['value'] = song.title
            results.append(song_json)

        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# WebAPP
class IndexView(View):
    template_name = 'music/index.html'

    def get(self, request):
        return render(request, self.template_name)


class SongView(generic.ListView):
    template_name = 'music/song_index.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.all()


class DetailSongView(generic.DetailView):
    model = Song
    template_name = 'music/song_detail.html'


class SongCreate(CreateView):
    model = Song
    fields = ['user', 'title', 'artist', 'album']


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('song-index')


class UserView(generic.ListView):
    template_name = 'music/user_index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()


class DetailUserView(generic.DetailView):
    model = User
    template_name = "music/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)

        # Get all Songs that current User doesnt Like
        excluded_user = User.objects.get(username=context.get('user'))
        context["song"] = Song.objects.exclude(user=excluded_user)

        f =[{'title': u'Jump'}, {'title': u"I Don't Want to Miss a Thing"}, {'title': u'Bohemian Rhapsody'}, {'title': u'Visions'}, {'title': u'My Song'}, {'title': u'Blood and Thunder'}, {'title': u'Teste'}]
        x = []

        x.append(f[0].get('title').title()
)

        return context


class UserCreate(View):
    form_class = UserForm
    template_name = "music/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            return redirect('user-index')


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user-index')


def add_new_favorite_song(request, pk):

    user = get_object_or_404(User, pk=pk)
    try:
        favorite_song = Song.objects.get(title=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/user_detail.html', {
            'user': user,
            'error_message': 'Please Select a Valid Song',
        })
    else:
        favorite_song.user.add(user)
        favorite_song.save()

    return render(request, 'music/user_detail.html', {'user': user})
