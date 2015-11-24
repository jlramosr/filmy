from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

from countries_app.models import Country
from languages_app.models import Language

#Almacenamientos principales
class Storage(models.Model):
    identifier = models.CharField(max_length=15, unique=True, blank=False, null=False, verbose_name=u'ID', help_text=u'Unique identifier of the storage unit')
    device_id = models.ForeignKey('Device', db_column='device_id' ,verbose_name=u'Device', null=True, related_name='storages_device', on_delete=models.SET_NULL, help_text=u'Device')
    is_original = models.BooleanField(verbose_name=u'Original', default=False)

    def __str__(self):
        return unicode(self.identifier).encode('utf-8')
    
    def __unicode__(self):
        return '%s' % (self.identifier,)
 
#Lineas de almacenamiento individual para registro principal
class StorageLine(models.Model):
    video_id = models.ForeignKey('Video', db_column='video_id', verbose_name=u'Video id', on_delete=models.CASCADE, related_name='storagelines_video', help_text=u'The internal identifier of the video associated to this line')
    storage_id = models.ForeignKey('Storage', db_column='storage_id', verbose_name=u'ID', blank=True, null=True, on_delete=models.SET_NULL, related_name='storagelines_storage', help_text=u'Main external identifier of the video associated to this line')
    format_id = models.ForeignKey('VideoInfo', db_column='format_id', verbose_name=u'Format', blank=True, null=True, on_delete=models.SET_NULL, related_name='storagelines_format', help_text=u'Video format')
    audio_id = models.ForeignKey('AudioInfo', db_column='audio_id', verbose_name=u'Audio', blank=True, null=True, on_delete=models.SET_NULL, related_name='storagelines_audio', help_text=u'Audio Format')
    languages = models.ManyToManyField('languages_app.Language', verbose_name=u'Languages', blank=True, null=True, related_name='storagelines_language')
    subtitles = models.ManyToManyField('languages_app.Language', verbose_name=u'Subtitles', blank=True, null=True, related_name='storagelines_subtitle')

    class Meta:
        unique_together = (('video_id', 'storage_id'), )
        verbose_name = u'Storage Line'
        verbose_name_plural = u'Storage Lines'

    def __str__(self):
        return unicode(self.video_id + ', ' + self.storage_id).encode('utf-8')
    
    def __unicode__(self):
        return '%s, %s' % (self.video_id, self.storage_id)

#DVD, Disco duro, etc ...
class Device(models.Model):
    name = models.CharField(max_length=31, verbose_name=u'Name', unique=True, help_text=u'Device\'s name')

    def __str__(self):
        return unicode(self.name).encode('utf-8')
 
    def __unicode__(self):
        return '%s' % (self.name,)

#Formatos de audio
class AudioInfo(models.Model):
    name = models.CharField(max_length=31, verbose_name=u'Name', unique=True, help_text=u'Name of audio\'s format')

    def __str__(self):
        return unicode(self.name).encode('utf-8')
    
    def __unicode__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name = u'Audio Data'
        verbose_name_plural = u'Audio Data'
 
#Formatos de video
class VideoInfo(models.Model):
    name = models.CharField(max_length=31, verbose_name=u'Name', unique=True, help_text=u'Name of video\'s format')

    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name = u'Video Data'
        verbose_name_plural = u'Video Data'


#Categorias de los videos (Pelicula, Serie, Documental, etc)
class Category(models.Model):
    name = models.CharField(max_length=31, verbose_name=u'Name', unique=True)
    icon = models.ImageField(upload_to='icons', verbose_name=u'Icon', blank=True)

    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name_plural = u'Categories'

#Actores y/o Directores
class Person(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Name', unique=True)
    is_actor = models.BooleanField(verbose_name=u'Actor', default=False)
    is_director = models.BooleanField(verbose_name=u'Director', default=False)
    photo = models.ImageField(upload_to='persons', verbose_name=u'Photo', blank=True)

    def __str__(self):
        return unicode(self.name).encode('utf-8')
    
    def __unicode__(self):
        return '%s' % (self.name,)

    class Meta:
        verbose_name = u'Artist'
        verbose_name_plural = u'Artists'

#Registros principales de la filmy
class Video(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'Create Date', blank=True, editable=False)
    write_date = models.DateTimeField(auto_now=True, verbose_name=u'Write Date', blank=True, editable=False)
    title = models.CharField(max_length=255, verbose_name=u'Title', blank=True)
    original_title = models.CharField(max_length=255, verbose_name=u'Original Title', blank=True)
    poster = models.ImageField(upload_to='filmy/posters', verbose_name=u'Poster', blank=True)
    categories = models.ManyToManyField('Category', verbose_name=u'Category', blank=True, null=True, related_name='videos_category')
    directors = models.ManyToManyField('Person', verbose_name=u'Director', blank=True, null=True, limit_choices_to={'is_director': True}, related_name='videos_director')
    cast = models.ManyToManyField('Person', verbose_name=u'Cast', blank=True, null=True, limit_choices_to={'is_actor': True}, related_name='videos_cast')
    nationalities = models.ManyToManyField('countries_app.Country', verbose_name=u'Nationality', blank=True, null=True, related_name='videos_nationality')
    duration = models.IntegerField(verbose_name=u'Duration(min.)', blank=True, null=True)
    is_byn = models.BooleanField(verbose_name=u'ByN', default=False)
    is_color = models.BooleanField(verbose_name=u'Color', default=False)
    summary = models.TextField(verbose_name=u'Summary', blank=True, null=True)
    evaluation_general = models.FloatField(verbose_name=u'General Evaluation', blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    tags = models.CharField(max_length=255, verbose_name=u'Tags', blank=True)
    notes = models.TextField(verbose_name=u'Notes', blank=True)
    last_vision_date = models.DateField(verbose_name=u'Last Vision Date', blank=True, null=True)
    episode_numbers = models.IntegerField(verbose_name=u'Episodes\'s number', blank=True, null=True)
    
    owner = models.ForeignKey('auth.User', related_name='videos_owner', verbose_name=u'Owner') #user who created the code snippet
    
    def __str__(self):
        return unicode(self.title).encode('utf-8')

    def __unicode__(self):
        return' %s' % (self.title,)

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
