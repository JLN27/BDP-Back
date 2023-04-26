from django.contrib import admin
from .models import PlayList, Song, Artist
from .forms import PlayListForm

class PlayListAdmin(admin.ModelAdmin):
    form = PlayListForm
    filter_horizontal = ('songs',)

admin.site.register(PlayList, PlayListAdmin)

admin.site.register(Song)
admin.site.register(Artist)