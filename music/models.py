# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Song(models.Model):
    user = models.ManyToManyField(User, blank=True)
    title = models.CharField(max_length=200, blank=True)
    artist = models.CharField(max_length=200, blank=True)
    album = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('song-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
