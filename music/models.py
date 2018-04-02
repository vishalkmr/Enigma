from django.contrib.auth.models import Permission, User,AbstractBaseUser,BaseUserManager
from django.db import models
# for validatrions
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import time
localtime = time.localtime(time.time())

def validate_image(value):
    s=str(value)
    s=s.lower()
    l=s.split('.')
    if not(l.__contains__('jpg')) and not(l.__contains__('png'))  and not(l.__contains__('gif')) and not(l.__contains__('ico')) and not(l.__contains__('bmp')):
        raise ValidationError(
            _('Image must be in following format : jpg,png,ico,bmp,gif')
        )

def validate_audio(value):
    s=str(value)
    s = s.lower()
    l=s.split('.')
    if not(l.__contains__('mp3'))  and not(l.__contains__('mp4'))and not(l.__contains__('avi')) :
        raise ValidationError(
            _('Audio file must be in following format : mp3,mp4,avi')
        )

def validate_year(value):
    if value >int(localtime[0]) or value <=1800:
        raise ValidationError(
            _('Published Year must be in range of 1800 -'+str(localtime[0]))
        )

def user_song_relationship_genrator(s):
    all_user = User.objects.all()
    # song = Song.objects.filter(pk=str(songid))
    for user in all_user:
        obj = UserSongRelationship(user_id=user.id,song=s)
        obj.save()
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




class Album(models.Model):
    album_title = models.CharField(max_length=500,unique=True)
    album_logo = models.ImageField(upload_to='static/album_logo/',verbose_name=album_title,validators=[validate_image])
    pub_year = models.IntegerField(validators=[validate_year],default=localtime[0])
    def __str__(self):
        return self.album_title+' '+str(self.pub_year)
    def __repr__(self):
        return self.album_title+' '+str(self.pub_year)

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250,unique=True)
    artist = models.CharField(max_length=250)
    audio_file = models.FileField(upload_to='static/songs/',validators=[validate_audio])
    genre_list = (('Bollywood','Bollywood'),('Dance','Dance'),('English','English'),('Hindi','Hindi'),('Hip-Hop','Hip-Hop'),('Love','Love'),('Pop','Pop'),('Punjabi','Punjabi'),('Remix','Remix'),('Rock','Rock'),('Soundtrack','Soundtrack'))
    genre= models.CharField(max_length=20,choices=genre_list,default='Bollywood',)

    def __str__(self):
        return self.song_title
    def save(self, *args,**kwargs):

        super(Song,self).save(*args,**kwargs)
        try:
            user_song_relationship_genrator(self)
        except:
            print('entgrity on song saving due to user_song_relationship_genrator ')
        finally:
            print("UserSong relastionship created")

class UserSongRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    song=models.ForeignKey(Song, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_added_to_playlist= models.BooleanField(default=False)
    listen_count=models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)+"  "+str(self.song)

    def save(self, *args,**kwargs):
        super(UserSongRelationship,self).save(*args,**kwargs)
        csv_generatore()

    class Meta:
        unique_together = ("user","song" )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male', )
    date_of_birth = models.DateField(default='2012-12-12')
    city = models.CharField(max_length=20,  default='Gurgaon' )



    def __str__(self):
        return str(self.user)+' '+str(self.gender)


class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    city=models.CharField(max_length=100)
    message=models.TextField(max_length=1000)
    def __str__(self):
        return str(self.name)+' '+str(self.message)

