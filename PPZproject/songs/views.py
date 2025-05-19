from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from songs.models import Song, Genre, Playlist
from songs.forms import PlaylistForm
from django.shortcuts import render, redirect
from songs.forms import SongForm

def home(request):
    songs = Song.objects.all().order_by('-id')[:6]
    genres = Genre.objects.all()
    return render(request, 'songs/home.html', {
        'title': 'Music Django - Home',
        'songs': songs,
        'genres': genres,
    })

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)  # не забувай request.FILES!
        if form.is_valid():
            form.save()
            return redirect('songs:index')  # або інший url після успішного додавання
    else:
        form = SongForm()
    return render(request, 'songs/add_song.html', {'form': form})

def index(request):
    songs = Song.objects.all().order_by('title')
    genres = Genre.objects.all()
    return render(request, 'songs/index.html', {
        'title': 'Music Django - Головна',
        'songs': songs,
        'genres': genres,
    })

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'songs/song_detail.html', {
        'title': f'Music Django - {song.title}',
        'song': song,
    })

def genre_filter(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = Song.objects.filter(genre=genre).order_by('title')
    genres = Genre.objects.all()
    return render(request, 'songs/index.html', {
        'title': f'Music Django - Жанр: {genre.name}',
        'songs': songs,
        'genres': genres,
        'selected_genre': genre,
    })

@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'songs/playlist_list.html', {
        'title': 'Music Django - Мої плейлисти',
        'playlists': playlists,
    })

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist.owner != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Ви не маєте прав на перегляд цього плейлиста")
    return render(request, 'songs/playlist_detail.html', {
        'title': f'Music Django - Плейлист: {playlist.name}',
        'playlist': playlist,
    })

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            print(f'Playlist created with owner: {playlist.owner}')
            return redirect('songs:playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistForm()

    return render(request, 'songs/create_playlist.html', {
        'title': 'Music Django - Створити плейлист',
        'form': form,
    })

@login_required
def add_song_to_playlist(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        if playlist_id:
            playlist = get_object_or_404(Playlist, id=playlist_id)
            if playlist.owner != request.user:
                return HttpResponseForbidden("Ви не маєте прав на редагування цього плейлиста")
            playlist.songs.add(song)
            return redirect('songs:playlist_detail', playlist_id=playlist.id)

    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'songs/add_songs_to_playlist.html', {
        'title': f'Music Django - Додати пісню "{song.title}" до плейлиста',
        'song': song,
        'playlists': playlists,
    })

@login_required
def add_songs_to_playlist_form(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist.owner != request.user:
        return HttpResponseForbidden("Ви не маєте прав на редагування цього плейлиста")

    if request.method == 'POST':
        song_ids = request.POST.getlist('songs')
        if song_ids:
            songs = Song.objects.filter(id__in=song_ids)
            for song in songs:
                playlist.songs.add(song)
            return redirect('songs:playlist_detail', playlist_id=playlist.id)

    available_songs = Song.objects.exclude(id__in=playlist.songs.values_list('id', flat=True))

    return render(request, 'songs/add_songs_to_playlist.html', {
        'title': f'Додати пісні до плейлиста {playlist.name}',
        'playlist': playlist,
        'available_songs': available_songs,
        'song': None,
        'playlists': None,
    })

@login_required
def remove_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist.owner != request.user:
        return HttpResponseForbidden("Ви не маєте прав на видалення цього плейлиста")

    if request.method == 'POST':
        playlist.delete()
        return redirect('songs:playlist_list')

    return redirect('songs:playlist_list')


@login_required
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song = get_object_or_404(Song, id=song_id)
    if playlist.owner != request.user:
        return HttpResponseForbidden("Ви не маєте прав на редагування цього плейлиста")
    playlist.songs.remove(song)
    return redirect('songs:playlist_detail', playlist_id=playlist.id)
