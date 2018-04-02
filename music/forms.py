from django import forms
from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser

from .models import Album, Song,Profile,UserSongRelationship,Contact


# class AlbumForm(forms.ModelForm):

#     class Meta:
#         model = Album
#         fields = ['artist', 'album_title', 'genre', 'album_logo']


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email','city','message']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'city', 'date_of_birth']





