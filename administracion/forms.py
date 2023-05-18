from django import forms
from .models import Song, PlayList, Artist, Event
from django.contrib.admin.widgets import FilteredSelectMultiple

class PlayListForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=FilteredSelectMultiple('Canciones', is_stacked=False),
        required=False,
    )

    class Meta:
        model = PlayList
        fields = ('name', 'songs')
        labels = {
            'name': 'Nombre',
            'songs': 'Canciones',
        }


class EventForm(forms.ModelForm):
    artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=FilteredSelectMultiple('Artistas', is_stacked=False),
        required=False,
    )

    class Meta:
        model = Event
        fields = ('name', 'place', 'date', 'artists')
        labels = {
            'name': 'Nombre',
            'place': 'Lugar',
            'date' : 'Fecha',
            'artists' : 'Artistas',
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'image', 'audio', 'video', 'artist')
        labels = {
            'title': 'Título',
            'image': 'Imagen',
            'audio': 'Audio',
            'video': 'Video',
            'artist': 'Artista',
        }

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'realName', 'birthDate', 'info', 'image')
        labels = {
            'name': 'Nombre',
            'realName': 'Nombre real',
            'birthDate': 'Fecha de nacimiento',
            'info': 'Información',
            'image': 'Imagen',
        }