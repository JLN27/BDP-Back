from django import forms
from .models import Song, PlayList, Artist, Event
from django.contrib.admin.widgets import FilteredSelectMultiple

class PlayListForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=FilteredSelectMultiple('Songs', is_stacked=False),
        required=False,
    )

    class Meta:
        model = PlayList
        fields = ('name', 'songs')


class EventForm(forms.ModelForm):
    artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=FilteredSelectMultiple('Artist', is_stacked=False),
        required=False,
    )

    class Meta:
        model = Event
        fields = ('name', 'place', 'date', 'artists')