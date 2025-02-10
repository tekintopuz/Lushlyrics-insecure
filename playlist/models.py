from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PlaylistUser(models.Model):
    class Meta:
        verbose_name_plural = _('Playlist Users')
        verbose_name = _('Playlist User')
        db_table = "playlistusers"
        ordering = ["-pk"]

    username = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name=_("Is Active?"))
    is_deleted = models.BooleanField(default=False, blank=True, null=True, verbose_name=_("Is Deleted?"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Deleted At"))
    def __str__(self):
        return f'Username = {self.username}, Liked Songs = {list(self.playlistsong_set.all())}'

class PlaylistSong(models.Model):
    class Meta:
        verbose_name_plural = _('Playlist Songs')
        verbose_name = _('Playlist Song')
        db_table = "playlistsongs"
        ordering = ["-pk"]

    user = models.ForeignKey(PlaylistUser, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=200)
    song_youtube_id =  models.CharField(max_length=20)
    song_albumsrc = models.CharField(max_length=255)
    song_dur = models.CharField(max_length=7)
    song_channel = models.CharField(max_length=100)
    song_date_added = models.CharField(max_length=12)

    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name=_("Is Active?"))
    is_deleted = models.BooleanField(default=False, blank=True, null=True, verbose_name=_("Is Deleted?"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Deleted At"))
    def __str__(self):
      return f'Title = {self.song_title}, Date = {self.song_date_added}'


