from django import forms
from .models import Playlist
from .models import Song


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'category']
        labels = {
            'name': 'Назва плейлисту',
            'category': 'Категорія',
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'genre', 'release_date', 'image']