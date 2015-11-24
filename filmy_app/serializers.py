from django.forms import widgets
from django.contrib.auth.models import User 

from filmy_app.models import Video, Category, Person, VideoInfo, AudioInfo, Storage, StorageLine, Device
from countries_app.models import Country
from languages_app.models import Language

from rest_framework import serializers

#from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth import get_user_model
#User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #videos = serializers.HyperlinkedRelatedField(many=True, view_name='video-detail')
    videos_owner = serializers.SlugRelatedField(many=True, slug_field='title', label=u'Videos', read_only=True)
    
    class Meta:
        model = User
        fields = ('url', 'username', 'videos_owner')
 
class CategorySerializer(serializers.HyperlinkedModelSerializer):  
    #videos = serializers.HyperlinkedRelatedField(many=True, view_name='video-detail')
    videos_category = serializers.SlugRelatedField(many=True, slug_field='title', label=u'Videos', read_only=True)
    
    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'videos_category')

class PersonSerializer(serializers.HyperlinkedModelSerializer): 
    videos_director = serializers.SlugRelatedField(many=True, slug_field='title', label=u'Director Videos', read_only=True)
    videos_cast = serializers.SlugRelatedField(many=True, slug_field='title', label=u'Cast Videos', read_only=True)
    
    class Meta:
        model = Person
        fields = ('url', 'name', 'is_actor', 'is_director', 'videos_director', 'videos_cast')

class AudioInfoSerializer(serializers.HyperlinkedModelSerializer): 
    storagelines_audio = serializers.SlugRelatedField(many=True, slug_field='id', label=u'Storage Lines', read_only=True)
    
    class Meta:
        model = AudioInfo
        fields = ('url', 'name', 'storagelines_audio')

class VideoInfoSerializer(serializers.HyperlinkedModelSerializer):
    storagelines_format = serializers.SlugRelatedField(many=True, slug_field='id', label=u'Storage Lines', read_only=True)
    
    class Meta:
        model = VideoInfo
        fields = ('url', 'name', 'storagelines_format')

class StorageLineSerializer(serializers.HyperlinkedModelSerializer):
    video_id = serializers.SlugRelatedField(many=False, slug_field='title', label=u'Video')
    storage_id = serializers.SlugRelatedField(many=False, slug_field='identifier', label=u'Storage')
    format_id = serializers.SlugRelatedField(many=False, slug_field='name', label=u'Format')
    audio_id = serializers.SlugRelatedField(many=False, slug_field='name', label=u'Audio Format')
    languages = serializers.SlugRelatedField(many=True, slug_field='name')
    subtitles = serializers.SlugRelatedField(many=True, slug_field='name')

    class Meta:
        model = StorageLine
        fields = ('url', 'video_id', 'storage_id', 'format_id', 'audio_id', 'languages', 'subtitles')

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    #device_id = serializers.HyperlinkedRelatedField(many=False, view_name='device-detail')
    device_id = serializers.SlugRelatedField(many=False, label=u'Device', slug_field='name')
    storagelines_storage = serializers.SlugRelatedField(many=True, slug_field='id', label=u'Storage Lines', read_only=True)
    
    class Meta:
        model = Storage
        fields = ('url', 'identifier', 'device_id', 'is_original', 'storagelines_storage')
        #fields = ('url', 'identifier', 'is_original', 'storageline_storage')

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    #storage_device = serializers.SlugRelatedField(many=True, slug_field='identifier', label=u'Storage', read_only=True)
    storages_device = StorageSerializer(many=True, label=u'Storage', read_only=True)
    
    class Meta:
        model = Device
        fields = ('url', 'name', 'storages_device')

class LanguageSerializer(serializers.HyperlinkedModelSerializer): 
    storagelines_language = serializers.SlugRelatedField(many=True, slug_field='id', label=u'Storage Line', read_only=True)
    storagelines_subtitle = serializers.SlugRelatedField(many=True, slug_field='id', label=u'Storage Line', read_only=True)
    
    class Meta:
        model = Language
        fields = ('url', 'name', 'storagelines_language', 'storagelines_subtitle')

class CountrySerializer(serializers.HyperlinkedModelSerializer): 
    #video_nationalities = serializers.HyperlinkedRelatedField(many=True, view_name='video-detail')
    videos_nationality = serializers.SlugRelatedField(many=True, slug_field='title', label=u'Videos', read_only=True)
    
    class Meta:
        model = Country
        fields = ('url', 'printable_name', 'videos_nationality')

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    #categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail')
    categories = serializers.SlugRelatedField(many=True, slug_field='name')
    #directors = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')
    directors = serializers.SlugRelatedField(many=True, slug_field='name')
    #cast = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')
    cast = serializers.SlugRelatedField(many=True, slug_field='name')
    #nationalities = serializers.HyperlinkedRelatedField(many=True, view_name='country-detail')
    #nationalities = CountrySerializer(many=True)
    nationalities = serializers.SlugRelatedField(many=True, slug_field='printable_name')
    #owner = serializers.Field(source='owner.username')
    owner = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)
    storagelines_video = StorageLineSerializer(many=True, label=u'Storage Lines', read_only=True)
    small_poster = serializers.SerializerMethodField('get_small_poster_url')
    
    class Meta:
        model = Video
        fields = ('url', 'id', 'owner',
		'create_date', 'write_date', 'title', 'original_title', 'duration', 'is_byn', 'is_color', 
		'categories', 'directors', 'cast', 'nationalities',
                'summary', 'evaluation_general', 'tags', 'notes', 'last_vision_date', 'episode_numbers',
		'storagelines_video', 'poster', 'small_poster')

    def get_small_poster_url(self, obj):
        options = {'size': (200, 180), 'crop': True}
        try:
            return obj.poster.get_thumbnail(options).url
        except:
            return ""

