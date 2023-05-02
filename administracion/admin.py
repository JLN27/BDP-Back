from django.contrib import admin
from .models import PlayList, Song, Artist, Event
from .forms import PlayListForm, EventForm

class PlayListAdmin(admin.ModelAdmin):
    form = PlayListForm
    filter_horizontal = ('songs',)

admin.site.register(PlayList, PlayListAdmin)

admin.site.register(Song)
admin.site.register(Artist)

class EventAdmin(admin.ModelAdmin):
    form = EventForm
    filter_horizontal = ()

admin.site.register(Event, EventAdmin)