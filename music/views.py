from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Song, Album, Profile,UserSongRelationship,Contact
from django.contrib.auth.models import Permission, User, AbstractUser
from .forms import UserForm, ProfileForm,ContactForm
from django.contrib.auth import authenticate, login, logout

from Recommenders import Popularity,Collaborative_Filtering,Clustering
import numpy as np
import pandas as pd
login_user_details = {}


import csv

def csv_generatore():
    all_users = User.objects.all()
    all_usersongrelationship = UserSongRelationship.objects.all()
    all_profile = Profile.objects.all()
    #songs.csv
    all_songs = Song.objects.all()
    with open('songs.csv','w') as new_file:
        new_file.write('song_id,album_id,song_title,artist,genre\n')
        for song in all_songs:
            delimiter=','
            line=str(song.id)+delimiter+str(song.album.id)+delimiter+str(song.song_title)+delimiter+str(song.artist)+delimiter+str(song.genre)+str('\n')
            new_file.write(line)


    # albums.csv
    all_albums = Album.objects.all()
    with open('albums.csv','w') as new_file:
        new_file.write('album_id,album_title,pub_year\n')
        for album in all_albums:
            delimiter=','
            line=str(album.id)+delimiter+str(album.album_title)+delimiter+str(album.pub_year)+str('\n')
            new_file.write(line)


    # users.csv
    all_users = Profile.objects.all()
    with open('users.csv', 'w') as new_file:
        new_file.write('user_id,username,email,gender,city,date_of_birth\n')
        for user in all_users:
            delimiter = ','
            line =str(user.user.id)+delimiter+ str(user.user.username) + delimiter + str(user.user.email) + delimiter + str(user.gender)+ delimiter + str(user.city)+ delimiter + str(user.date_of_birth)+ str(
                '\n')
            new_file.write(line)


    # usersongrelationships.csv
    all_userssongs = UserSongRelationship.objects.all()
    with open('usersongrelationships.csv', 'w') as new_file:
        new_file.write('user_id,song_id,is_favorite,is_added_to_playlist,listen_count\n')
        for userssong in all_userssongs:
            delimiter = ','
            line = str(userssong.user.id)+delimiter+str(userssong.song.id)+delimiter+ str(userssong.is_favorite) + delimiter + str(userssong.is_added_to_playlist) + delimiter + str(
                userssong.listen_count) + str(
                '\n')
            new_file.write(line)









def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/index_unregister.html')
    else:
        all_albums = Album.objects.all()
        all_songs = Song.objects.all()
        csv_generatore()
        status = 'normal'
        query = request.GET.get("querry")
        if query:
            status = 'query'
            searched_albums = all_albums.filter(album_title__icontains=query).distinct()
            searched_songs = all_songs.filter(song_title__icontains=query).distinct()
            searched_artists = all_songs.filter(artist__contains=query).distinct()
            searched_genres = all_songs.filter(genre__contains=query).distinct()
            return render(request, 'music/index.html',
                          {'searched_albums': searched_albums, 'searched_songs': searched_songs,
                           'searched_artists': searched_artists, 'searched_genres': searched_genres, 'status': status})
        context = {'all_albums': all_albums, 'all_songs': all_songs, 'status': status,'user_status':request.session['status']}
        # context.update(csrf(request))
        return render(request, 'music/index.html', context)


# display list of albums
def albums(request):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()
        all_albums = Album.objects.all()
        latest_albums=[]
        #latest albums
        a=Album.objects.order_by('pub_year')
        for i in a[::-1]:
            latest_albums.append(i)

        #popular albums
        popular_albums=[]
        obj=Popularity()
        popular=obj.recommend_album()

        for album in popular['album_title'] :
            a = Album.objects.get(album_title=album)
            popular_albums.append(a)


        # creating Collaborative_Filtering object
        cf_obj = Collaborative_Filtering(request.session['username'])
        cf=cf_obj.recommend_album()
        # cf recommended songs
        cf_albums = []

        for title in cf['album_title'] :
            a = Album.objects.get(album_title=title)
            cf_albums.append(a)


        ls=set()
        class Realese_year():
            def __init__(self,name=None,albums=None,more_albums=None,much_more_albums=None,count=None):
                self.name=name
                self.albums=albums
                self.more_albums=more_albums
                self.much_more_albums = much_more_albums
                if(count>18):
                    count=18
                self.count=count
        for s in all_albums:
            ls.add(s.pub_year)
        year=[]
        ls=list(ls)
        ls.sort()
        for y in ls:
            l=Album.objects.filter(pub_year=y).distinct()
            s=Realese_year(y,l[:6],l[6:12],l[12:18],len(l))
            year.append(s)





        context = {'all_albums': all_albums[:6], 'latest_albums':latest_albums[:6],'more_latest_albums':latest_albums[6:12],'popular_albums':popular_albums[:6],'more_popular_albums':popular_albums[6:12],'id':request.session['user_id'],'cf_albums':cf_albums[:6],'more_cf_albums':cf_albums[6:12],'year':year,'user_status':request.session['status']}
        return render(request, 'music/albums.html', context)


# display details of given album
def album_detail(request, album_id):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()
        all_albums = Album.objects.all()
        all_songs = Song.objects.all()
        try:
            album = Album.objects.get(pk=album_id)
            usersongs = UserSongRelationship.objects.filter(user_id=request.session['user_id'],song__album=album)

        except Album.DoesNotExist:
            return redirect('music:albums')


        # creating Collaborative_Filtering object
        cf_obj = Collaborative_Filtering(request.session['username'])
        cf=cf_obj.similar_album(album.album_title)

        # similar songs
        cf_based_similar_albums = []
        for title in cf['album_title'] :
            a = Album.objects.get(album_title=title)
            cf_based_similar_albums.append(a)

        # creating Clustering object
        cl_obj = Clustering(request.session['username'])
        cl=cl_obj.similar_album(album.album_title)

        # similar songs
        cl_based_similar_albums = []
        for title in cl['album_title'] :
            a = Album.objects.get(album_title=title)
            cl_based_similar_albums.append(a)

        # list of songs of that album
        songs = Song.objects.filter(album=album)


        ls=set()
        class Genre():
            def __init__(self,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                self.count=count
        for s in all_songs:
            ls.add(s.genre)
        genre=[]
        ls=list(ls)
        ls.sort()
        for g in ls:
            l=Song.objects.filter(genre=g).distinct()
            s=Genre(g,l[:6],l[6:12],l[12:18],len(l))
            genre.append(s)


        ls=set()
        class Artist():
            def __init__(self,id=None,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.id=id
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                self.count=count

        for s in all_songs:
            ls.add(s.artist)
        artist=[]
        ls=list(ls)
        ls.sort()
        c=0
        for a in ls:
            l=Song.objects.filter(artist=a).distinct()
            s=Artist(c,a,l[:6],l[6:12],l[12:18],len(l))
            artist.append(s)
            c=c+1




        context = {'all_albums': all_albums, 'all_songs': all_songs, 'songs': songs, 'album': album,'usersongs':usersongs,'id':request.session['user_id'],'cf_based_similar_albums':cf_based_similar_albums[:6],'more_cf_based_similar_albums':cf_based_similar_albums[6:12],'cl_based_similar_albums':cl_based_similar_albums[:6],'more_cl_based_similar_albums':cl_based_similar_albums[6:12],'artist':artist,'genre':genre,'user_status':request.session['status']}

        return render(request, 'music/album_details.html', context)


# display list of songs
def songs(request):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()
        context={}
        all_songs = Song.objects.all()
        latest_songs=[]
        #latest songs but from each album only one song
        a=Album.objects.order_by('pub_year')
        for i in a[::-1]:
            latest_songs.append(Song.objects.filter(album=i)[0])

        #popular songs
        popular_songs=[]
        obj=Popularity()
        popular=obj.recommend_song()
        for title in popular['song_title'] :
            song = Song.objects.get(song_title=title)
            popular_songs.append(song)


        # creating Collaborative_Filtering object
        cf_obj = Collaborative_Filtering(request.session['username'])
        cf=cf_obj.recommend_song()

        # cf recommended songs
        cf_songs = []
        for title in cf['song_title'] :
            song = Song.objects.get(song_title=title)
            cf_songs.append(song)

        ls=set()
        class Genre():
            def __init__(self,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                if(count>18):
                    count=18
                self.count=count
        for s in all_songs:
            ls.add(s.genre)
        genre=[]
        ls=list(ls)
        ls.sort()
        for g in ls:
            l=Song.objects.filter(genre=g).distinct()
            s=Genre(g,l[:6],l[6:12],l[12:18],len(l))
            genre.append(s)


        ls=set()
        class Artist():
            def __init__(self,id=None,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.id=id
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                self.count=count

        for s in all_songs:
            ls.add(s.artist)
        artist=[]
        ls=list(ls)
        ls.sort()
        c=0
        for a in ls:
            l=Song.objects.filter(artist=a).distinct()
            s=Artist(c,a,l[:6],l[6:12],l[12:18],len(l))
            artist.append(s)
            c=c+1


        context = {'all_songs': all_songs[:6],'id':request.session['user_id'],'popular_songs':popular_songs[:6],'latest_songs':latest_songs[:6],'more_latest_songs':latest_songs[6:12],'more_popular_songs':popular_songs[6:12],'cf_songs':cf_songs[:6],'more_cf_songs':cf_songs[6:12],'genre':genre,'artist':artist ,'user_status':request.session['status']}


        return render(request, 'music/songs.html', context)


# display details of given song
def song_detail(request, song_id):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()
        all_albums = Album.objects.all()
        all_songs = Song.objects.all()

        try:


            usersongs = UserSongRelationship.objects.filter(user_id=request.session['user_id'], song_id=song_id)
            usersong=usersongs[0]
        except Song.DoesNotExist:
            return redirect('music:songs')

        # creating Collaborative_Filtering object
        cf_obj = Collaborative_Filtering(request.session['username'])
        cf=cf_obj.similar_song(usersong.song.song_title)

        # similar songs
        cf_based_similar_songs = []
        for title in cf['song_title'] :
            song = Song.objects.get(song_title=title)
            cf_based_similar_songs.append(song)

        # creating Clustering object
        cl_obj = Clustering(request.session['username'])
        cl=cl_obj.similar_song(usersong.song.song_title)

        # similar songs
        cl_based_similar_songs = []
        for title in cl['song_title'] :
            song = Song.objects.get(song_title=title)
            cl_based_similar_songs.append(song)





        ls=set()
        class Genre():
            def __init__(self,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                if(count>18):
                    count=18
                self.count=count

        genre=[]

        l=Song.objects.filter(genre=usersong.song.genre).distinct()
        genre=Genre(usersong.song.genre,l[:6],l[6:12],l[12:18],len(l))



        ls=set()
        class Artist():
            def __init__(self,name=None,songs=None,more_songs=None,count=None):
                self.name=name
                self.songs=songs
                self.more_songs=more_songs
                self.count=count




        l=Song.objects.filter(artist=usersong.song.artist).distinct()
        artist=Artist(usersong.song.artist,l[:10],l[6:12],len(l))

        # print(artist)
        # for i in artist.songs:
        #     print(i)
        # print(genre)
        # for i in genre.songs:
        #     print(i)

        context = {'all_albums': all_albums, 'all_songs': all_songs, 'usersong':usersong,'id':request.session['user_id'],'cf_based_similar_songs':cf_based_similar_songs[:6],'more_cf_based_similar_songs':cf_based_similar_songs[6:12],'cl_based_similar_songs':cl_based_similar_songs[:6],'more_cl_based_similar_songs':cl_based_similar_songs[6:12],'genre':genre,'artist':artist,'user_status':request.session['status']}
        return render(request, 'music/song_details.html', context)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('music:index')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    u = User.objects.get(username=username)
                    request.session['status']=u.is_superuser
                    request.session['username'] = u.username
                    request.session['first_name'] = u.first_name
                    request.session['last_name'] = u.last_name
                    request.session['email'] = u.email
                    request.session['password'] = u.password
                    request.session['user_id'] = u.id

                    return render(request, 'music/index.html', {'success_message': 'Welcome ' + username + ' !','user_status':request.session['status']})
                else:
                    return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'music/login.html', {'error_message': 'Invalid Login Credentials '})
        return render(request, 'music/login.html')


def login_test_user(request):
    if request.user.is_authenticated:
        return redirect('music:index')
    else:
        u = User.objects.get(username='Testuser')
        user = authenticate(username='Testuser', password='pass@123')
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['status']=False
                request.session['username'] = u.username
                request.session['first_name'] = u.first_name
                request.session['last_name'] = u.last_name
                request.session['email'] = u.email
                request.session['password'] = u.password
                request.session['user_id'] = u.id

                return render(request, 'music/index.html', {'success_message': 'You are successfully Login as ' + u.username + ' !','warning_message':'Testuser is an shared account so you may not get best recomendations !','info_message':'For best recomendations we suggests you to create an account .','user_status':request.session['status']})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your Testuser account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid Login Testuser Credentials '})


def logout_user(request):
    csv_generatore()    
    username=''
    try:
        username=request.session['username']
    except:
        username='You'

    request.session.flush()
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
        'success_message': 'You are succesfully logout !'
    }
    return render(request, 'music/index_unregister.html', context)


def create_account(request):
    if request.user.is_authenticated:
        return redirect('music:index')
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    u = User.objects.get(username=username)
                    request.session['username'] = u.username
                    request.session['first_name'] = u.first_name
                    request.session['last_name'] = u.last_name
                    request.session['email'] = u.email
                    request.session['password'] = u.password
                    request.session['user_id'] = u.id
                    # creating coresponding profile
                    p = Profile(user_id=request.session['user_id'])
                    p.save()
                    print('New user account is created ')
                    user_song_relationship_genrator(request.session['user_id'])

                    return redirect('music:profile')
        context = {
            "form": form,

        }
        return render(request, 'music/create_account.html', context)


def user_song_relationship_genrator(userid):
    # user = User.objects.filter(pk=str(userid))
    all_songs = Song.objects.all()
    for song in all_songs:
        obj = UserSongRelationship(user_id=str(userid),song_id=song.id)
        obj.save()


def profile(request):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            city = form.cleaned_data['city']

            # edited coresponding profile
            p = Profile.objects.get(user_id=request.session['user_id'])
            p.gender = gender
            p.date_of_birth = date_of_birth
            p.city = city.lower()
            p.save()

            p = Profile.objects.get(user_id=request.session['user_id'])
            if p.date_of_birth is not '1111-11-11':
                status = 'created'
            else:
                status = 'new'
            context = {
                "form": form,
                "username": request.session['username'],
                "gender": p.gender,
                "city": p.city,
                "date": p.date_of_birth,
                "status": status,
               "user_status":request.session['status']
            }
            return render(request, 'music/profile.html', context)

            return render(request, 'music/profile.html')
        p = Profile.objects.get(user_id=request.session['user_id'])
        if p.date_of_birth is not '1111-11-11':
            status='created'

        else:
            status='new'


        context = {
            "form": form,
            "username": request.session['username'],
            "gender": p.gender,
            "city": p.city,
            "date":p.date_of_birth,
            "status" :status,
            "user_status": request.session['status']
        }
        return render(request, 'music/profile.html', context)


def favorite_add(request, song_id):
    us = UserSongRelationship.objects.get(user_id=request.session['user_id'], song_id=song_id)
    try:
        if us.is_favorite:
            us.is_favorite = False
        else:
            us.is_favorite = True
        us.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def listen_count_add(request, song_id):
    us = UserSongRelationship.objects.get(user_id=request.session['user_id'], song_id=song_id)
    try:
        us.listen_count=us.listen_count+1
        us.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def playlist_add(request, string):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        song_id=string[:-1]
        page=string[-1]
        us=UserSongRelationship.objects.get(user_id=request.session['user_id'],song_id=song_id)
        if us.is_added_to_playlist:
            us.is_added_to_playlist = False
        else:
            us.is_added_to_playlist = True
        us.save()
        song = Song.objects.get(pk=song_id)
        if page is 'S':
            return redirect('music:song_detail' ,song.id)
        elif page is 'A':
            return redirect('music:album_detail', song.album_id)
        else:
            return redirect('music:playlist')


def playlist(request):
    if not request.user.is_authenticated:
        return redirect('music:index')
    else:
        csv_generatore()        
        all_albums = Album.objects.all()
        all_songs = Song.objects.all()

        try:
            usersongs = UserSongRelationship.objects.filter(user_id=request.session['user_id']).order_by('listen_count')[::-1]
            playlist_items=[]
            for u in usersongs:
                if u.is_added_to_playlist:
                    playlist_items.append(u)
                    # print(u.listen_count)

        except Song.DoesNotExist:
            return redirect('music:songs')




        ls=set()
        class Artist():
            def __init__(self,id=None,name=None,songs=None,more_songs=None,much_more_songs=None,count=None):
                self.name=name
                self.id=id
                self.songs=songs
                self.more_songs=more_songs
                self.much_more_songs = much_more_songs
                self.count=count

        for s in all_songs:
            ls.add(s.artist)
        artist=[]
        ls=list(ls)
        ls.sort()
        c=0
        for a in ls:
            l=Song.objects.filter(artist=a).distinct()
            s=Artist(c,a,l[:6],l[6:12],l[12:18],len(l))
            artist.append(s)
            c=c+1



        context = {'all_albums': all_albums, 'all_songs': all_songs,'usersongs':playlist_items,'id':request.session['user_id'],'artist':artist,'user_status':request.session['status']}
        return render(request, 'music/playlist.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        city = form.cleaned_data['city']
        message = form.cleaned_data['message']
        c=Contact(name=name,email=email,city=city,message=message)
        c.save()
        context = {"form": form, 'success_message': 'Contact form successfully submitted !'}
    else:
        context = {"form": form, 'error_message': 'Contact form not submitted !'}
    if not request.user.is_authenticated:
        return render(request, 'music/index_unregister.html', context)
    else:
        context["user_status"]  =request.session['status']
        return render(request, 'music/index.html', context)



def search(request):
   if request.method=='GET':
       search_text=request.GET['search_text']
       # print(request.GET)
   else:
       search_text=None
   if search_text!='':
       searched_albums = Album.objects.filter(album_title__icontains=search_text).distinct()
       searched_songs = Song.objects.filter(song_title__icontains=search_text).distinct()
       searched_artists = Song.objects.filter(artist__icontains=search_text).distinct()
       searched_genres = Song.objects.filter(genre__contains=search_text).distinct()
       # print('non empty')
   else:
       searched_albums=[]
       searched_songs=[]
       searched_artists=[]
       searched_genres=[]
       # print('empty')
   # print('search_text'+search_text)
   context={'searched_albums':searched_albums,'searched_songs':searched_songs,'searched_artists':searched_artists,'searched_genres':searched_genres,'user_status':request.session['status']}
   return render(request, 'music/ajax_search.html', context)

def popularity(request):
   return render(request, 'music/popularity.html')


def collaborative_filtering(request):
   return render(request, 'music/Collaborative_Filtering.html')

def correlations(request):
   return render(request, 'music/Correlations.html')

def song_clustering(request):
   return render(request, 'music/Song_Clustering.html')

def album_clustering(request):
   return render(request, 'music/Album_Clustering.html')




def Users_Correlations(request):
    csv_generatore()
    import os
    os.system('python User_Correlations_Genratore.py')
    users = User.objects.all()


    context = {'users': users, }
    return render(request, 'music/Users_Correlations.html', context)


def Songs_Correlations(request):
    csv_generatore()
    import os
    os.system('python Song_Correlations_Genratore.py')
    songs = Song.objects.all()

    context = {'songs': songs, }
    return render(request, 'music/Songs Correlations.html', context)


def Albums_Correlations(request):
    csv_generatore()
    import os
    os.system('python Album_Correlations_Genratore.py')
    albums = Album.objects.all()
    context = {'albums': albums, }
    return render(request, 'music/Albums Correlations.html', context)
