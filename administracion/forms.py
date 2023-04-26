from django import forms
from .models import Song, PlayList, PlayListSong

class PlayListForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = PlayList
        fields = ('name', 'songs')