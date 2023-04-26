from django.db import models
from django.core.validators import FileExtensionValidator

class Artist(models.Model):
    name = models.CharField(max_length=200)
    realName = models.CharField(max_length=200)
    birthDate = models.DateField()
    info = models.CharField(max_length=400,null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=254)
    date = models.DateTimeField()

class EventArtist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('event', 'artist')

class Song(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    audio = models.FileField(upload_to='audio/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    video = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
class PlayList(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, through='PlayListSong')

    def __str__(self):
        return self.name

class PlayListSong(models.Model):
    playList = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playList', 'song')
