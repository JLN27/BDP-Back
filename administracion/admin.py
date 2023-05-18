from django.contrib import admin
from .models import PlayList, Song, Artist, Event
from .forms import PlayListForm, EventForm


class PlayListAdmin(admin.ModelAdmin):
    form = PlayListForm
    filter_horizontal = ('songs',)
    icon_name = 'playlist_play'

admin.site.register(PlayList, PlayListAdmin)



class EventAdmin(admin.ModelAdmin):
    form = EventForm
    icon_name = 'event'


admin.site.register(Event, EventAdmin)


class SongAdmin(admin.ModelAdmin):
    icon_name = 'music_note'


admin.site.register(Song, SongAdmin)


class ArtistAdmin(admin.ModelAdmin):
    icon_name = 'person'


admin.site.register(Artist, ArtistAdmin)

