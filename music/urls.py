from django.conf.urls import url

from . import views

urlpatterns = [
    # Main Page
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Songs
    url(r'songs/$', views.SongView.as_view(), name='song-index'),
    url(r'song/(?P<pk>[0-9]+)/$', views.DetailSongView.as_view(), name='song-detail'),
    url(r'song/add/$', views.SongCreate.as_view(), name='song-add'),
    url(r'song/(?P<pk>[0-9]+)/delete$', views.SongDelete.as_view(), name='song-delete'),

    # Users
    url(r'users/$', views.UserView.as_view(), name='user-index'),
    url(r'user/(?P<pk>[0-9]+)/$', views.DetailUserView.as_view(), name='user-detail'),
    url(r'user/add/$', views.UserCreate.as_view(), name='user-add'),
    url(r'user/(?P<pk>[0-9]+)/delete$', views.UserDelete.as_view(), name='user-delete'),

    # User Add New Favorite Song
    url(r'user/(?P<pk>[0-9]+)/favorite/$', views.add_new_favorite_song, name='favorite-song'),
]
