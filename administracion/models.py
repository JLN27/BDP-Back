from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import os

class Artist(models.Model):
    name = models.CharField(max_length=200)
    realName = models.CharField(max_length=200)
    birthDate = models.DateField()
    info = models.CharField(max_length=400,null=True)
    image = models.ImageField(upload_to='artist_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=254)
    date = models.DateTimeField()
    artists = models.ManyToManyField(Artist, through='EventArtist')


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
    
    def delete(self, *args, **kwargs):
        # Eliminar los archivos asociados a las instancias de FileField e ImageField
        if self.image:
            os.remove(self.image.path)
        if self.audio:
            os.remove(self.audio.path)
        if self.video:
            os.remove(self.video.path)
        # Llamar al método delete() original de la clase para eliminar la instancia
        super(Song, self).delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        # Si se está actualizando una instancia existente, elimina los archivos antiguos antes de guardar la instancia actualizada
        if self.id:
            old_instance = Song.objects.get(id=self.id)
            if old_instance.image and old_instance.image != self.image:
                os.remove(old_instance.image.path)
            if old_instance.audio and old_instance.audio != self.audio:
                os.remove(old_instance.audio.path)
            if old_instance.video and old_instance.video != self.video:
                os.remove(old_instance.video.path)
        # Llamar al método save() original de la clase para guardar la instancia actualizada
        super(Song, self).save(*args, **kwargs)

    
class PlayList(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, through='PlayListSong', blank=True, default=None)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PlayListSong(models.Model):
    playList = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playList', 'song')
