# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from music.models import Song
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class SongModelTests(TestCase):

    def test_string_representation(self):
        song = Song(title="Song Title")
        self.assertEqual(str(song), song.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Song._meta.verbose_name_plural), "songs")

    def get_absolute_url(self):
        song = Song.objects.create(title='1-title', artist='1-artist', album='1-album')
        self.assertIsNotNone(song.get_absolute_url())


class UserModelTests(TestCase):

    def test_string_representation(self):
        user = User(username="User Name")
        self.assertEqual(str(user), user.username)


class AppTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/music/')
        self.assertEqual(response.status_code, 200)


class SongViewTest(TestCase):

    def test_no_songs(self):
        response = self.client.get('/music/songs/')
        self.assertContains(response, 'No Songs in Database')

    def test_one_song(self):
        Song.objects.create(title='1-title', artist='1-artist', album='1-album')
        response = self.client.get('/music/songs/')
        self.assertContains(response, '1-title')

    def test_two_song(self):
        Song.objects.create(title='1-title', artist='1-artist', album='1-album')
        Song.objects.create(title='2-title', artist='2-artist', album='2-album')
        response = self.client.get('/music/songs/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '2-title')


class UserViewTest(TestCase):

    def test_no_entries(self):
        response = self.client.get('/music/users/')
        self.assertContains(response, 'No Users in Database')

    def test_one_entry(self):
        User.objects.create(username='1-user', email='1-email')
        response = self.client.get('/music/users/')
        self.assertContains(response, '1-user')

    def test_two_entry(self):
        User.objects.create(username='1-user', email='1-email')
        User.objects.create(username='2-user', email='2-email')
        response = self.client.get('/music/users/')
        self.assertContains(response, '1-user')
        self.assertContains(response, '2-user')


class SongCreateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Test Dummy')
        self.song = Song.objects.create(title='1-title', artist='1-artist', album='1-album')

    def test_basic_view(self):
        response = self.client.get(self.song.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_in_song(self):
        response = self.client.get(self.song.get_absolute_url())
        self.assertContains(response, self.song.title)

    def test_artist_in_song(self):
        response = self.client.get(self.song.get_absolute_url())
        self.assertContains(response, self.song.artist)

    def test_album_in_song(self):
        response = self.client.get(self.song.get_absolute_url())
        self.assertContains(response, self.song.album)


class AddSongtoUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Test Dummy')
        self.song = Song.objects.create(title='1-title', artist='1-artist', album='1-album')

    def add_song_to_user(self):
        favorite_song = Song.objects.get(title=self.song.title)
        favorite_song.user.add(self.user)
        favorite_song.save()

        self.assertEqual(favorite_song.user, self.user)


class SongListTest(APITestCase):

    def test_create_song(self):
        url = reverse('get-songs')
        data = {
            'title': '1-title',
            'album': '1-album',
            'artiste': '1-artist',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, '1-title')


class UserListTest(APITestCase):

    def test_create_song(self):
        url = reverse('get-users')
        data = {
            'username': 'Dummy Test',
            'email': 'dummy@test.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Dummy Test')
        