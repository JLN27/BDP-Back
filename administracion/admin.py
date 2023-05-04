from django.contrib import admin
from .models import PlayList, Song, Artist, Event
from .forms import PlayListForm, EventForm

class PlayListAdmin(admin.ModelAdmin):
    form = PlayListForm
    filter_horizontal = ('songs',)

admin.site.register(PlayList, PlayListAdmin)

admin.site.register(Song)


class EventAdmin(admin.ModelAdmin):
    form = EventForm

admin.site.register(Event, EventAdmin)

admin.site.register(Artist)
