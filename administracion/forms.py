from django import forms
from .models import Song, PlayList, Artist, Event

class PlayListForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = PlayList
        fields = ('name', 'songs')


class EventForm(forms.ModelForm):
    artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Event
        fields = ('name', 'place', 'date', 'artists')