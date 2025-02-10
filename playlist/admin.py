from django.contrib import admin
from playlist.models import PlaylistUser, PlaylistSong
from django.utils.translation import gettext_lazy as _

class PlaylistUserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username')
    list_display = ('id', 'username')
    model = PlaylistUser
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    'username',
                )}),
    )
    readonly_fields = ('id',)


class PlaylistSongAdmin(admin.ModelAdmin):
    search_fields = ('id',
                     'song_title',
                     'song_youtube_id',
                     'song_albumsrc',
                     'song_dur',
                     'song_channel',
                     'song_date_added',)
    list_display = ('id',
                    'song_title',
                    'song_youtube_id',
                    'song_albumsrc',
                    'song_dur',
                    'song_channel',
                    'song_date_added',)
    model = PlaylistSong
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    'user',
                    'song_title',
                    'song_youtube_id',
                    'song_albumsrc',
                    'song_dur',
                    'song_channel',
                    'song_date_added',

                )}),
    )
    readonly_fields = ('id',)

admin.site.register(PlaylistUser, PlaylistUserAdmin)
admin.site.register(PlaylistSong, PlaylistSongAdmin)