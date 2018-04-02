"""Enigma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include, re_path
from . import views
app_name = 'music'
urlpatterns = [

        path('', views.index, name='index'),
        # path('', views.IndexView.as_view(), name='index'),
        path('album/', views.albums, name='albums'),
        path('album/<int:album_id>', views.album_detail, name='album_detail'),
        path('song/', views.songs, name='songs'),
        path('song/<int:song_id>', views.song_detail, name='song_detail'),
        # path('song/<int:pk>', views.Song_Detail_View.as_view(), name='song_detail'),
        path('create_account/', views.create_account, name='create_account'),
        path('login_user/', views.login_user, name='login_user'),
        path('login_test_user/', views.login_test_user, name='login_test_user'),
        path('logout_user/', views.logout_user, name='logout_user'),
        path('profile/', views.profile, name='profile'),
        # path('profile_update/', views.profile_update, name='profile_update'),

        path('favorite_add/<int:song_id>', views.favorite_add, name='favorite_add'),
        path('listen_count_add/<int:song_id>', views.listen_count_add, name='listen_count_add'),
        path('playlist_add/<string>', views.playlist_add, name='playlist_add'),
        # path('playlist_add1/<string>', views.playlist_add1, name='playlist_add1'),
        path('playlist/', views.playlist, name='playlist'),
        path('contact/', views.contact, name='contact'),
        path('search/', views.search, name='search'),
        path('Popularity/', views.popularity, name='popularity'),
        path('Collaborative_Filtering/', views.collaborative_filtering, name='Collaborative_Filtering'),
        path('Correlations/', views.correlations, name='correlations'),
        path('Users_Correlations/', views.Users_Correlations, name='Users_Correlations'),
        path('Songs_Correlations/', views.Songs_Correlations, name='Songs_Correlations'),
        path('Albums_Correlations/', views.Albums_Correlations, name='Albums_Correlations'),
        path('Song_Clustering/', views.song_clustering, name='Song_Clustering'),
        path('Album_Clustering/', views.album_clustering, name='Album_Clustering'),

]

