from django.contrib import admin
from .models import PlayList, Song, Artist, Event
from .forms import PlayListForm, EventForm, SongForm, ArtistForm
class PlayListAdmin(admin.ModelAdmin):
    form = PlayListForm
    filter_horizontal = ('songs',)
    icon_name = 'person'


admin.site.register(PlayList, PlayListAdmin)



class EventAdmin(admin.ModelAdmin):
    form = EventForm
    icon_name = 'person'


admin.site.register(Event, EventAdmin)


class SongAdmin(admin.ModelAdmin):
    form = SongForm
    icon_name = 'music_note'
    

admin.site.register(Song, SongAdmin)


class ArtistAdmin(admin.ModelAdmin):
    form = ArtistForm
    icon_name = 'person'


admin.site.register(Artist, ArtistAdmin)