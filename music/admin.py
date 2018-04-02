from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Song,Album,User,UserSongRelationship,Contact
from .models import Profile
import random
import numpy as np
#creating an admin action
def empty_listen_count(modeladmin, request, queryset):
    queryset.update(listen_count=0)
def empty_all_fields(modeladmin, request, queryset):
    queryset.update(listen_count=0,is_favorite=False,is_added_to_playlist=False)
def add_to_playlist(modeladmin, request, queryset):
    queryset.update(is_added_to_playlist=True)
def add_to_favorite(modeladmin, request, queryset):
    queryset.update(is_favorite=True)
def randomize(modeladmin, request, queryset):
    queryset.update(is_favorite=random.choice([   'False','True']),is_added_to_playlist=random.choice(['True', 'False']),listen_count=random.randrange(1, 10))


empty_listen_count.short_description = "Empty Listen Count"
empty_all_fields.short_description = "Empty All Fields"
add_to_playlist.short_description = "Add To Playlist "
add_to_favorite.short_description = "Add To Favorite-list "
randomize.short_description = "Randomize"


#customizing the admin view
tabular_view=admin.TabularInline
inline_view=admin.StackedInline
class AlbumInline(inline_view):
    model = Song
    extra = 1

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_title', 'pub_year')
    inlines = [AlbumInline]

class SongAdmin(admin.ModelAdmin):

    list_display = ('song_title', 'album','artist','genre')

class UserSongAdmin(admin.ModelAdmin):

    list_display = ('user', 'song','is_favorite','is_added_to_playlist','listen_count')
    actions = [add_to_favorite,add_to_playlist,empty_listen_count,empty_all_fields,randomize]

class ContactAdmin(admin.ModelAdmin):

    list_display = ('name', 'email','city','message')


admin.site.register(Album,AlbumAdmin)
admin.site.register(Song,SongAdmin)
admin.site.register(UserSongRelationship,UserSongAdmin)
admin.site.register(Contact,ContactAdmin)


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
