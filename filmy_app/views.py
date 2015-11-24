from filmy_app.models import Video, Category, Person, VideoInfo, AudioInfo, Storage, StorageLine, Device
from filmy_app.serializers import UserSerializer, VideoSerializer, CategorySerializer, PersonSerializer, CountrySerializer, LanguageSerializer, VideoInfoSerializer, AudioInfoSerializer, StorageSerializer, StorageLineSerializer, DeviceSerializer
from filmy_app.permissions import IsOwnerOrReadOnly
from countries_app.models import Country
from languages_app.models import Language

from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

import django_filters

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "head.html"

class VideoFilter(django_filters.FilterSet):
    min_duration = django_filters.NumberFilter(name="duration", lookup_type='gte')
    max_duration = django_filters.NumberFilter(name="duration", lookup_type='lte')
    category = django_filters.CharFilter(name="categories__id")
    class Meta:
        model = Video
        fields = ['id', 'title', 'duration', 'min_duration', 'max_duration', 'category']

class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = ['id', 'name', 'is_actor', 'is_director']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VideoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filter_class = VideoFilter

    def pre_save(self, obj):
        obj.owner = self.request.user

class CountryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class LanguageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PersonViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_class = PersonFilter

class AudioInfoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AudioInfo.objects.all()
    serializer_class = AudioInfoSerializer

class VideoInfoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = VideoInfo.objects.all()
    serializer_class = VideoInfoSerializer

class StorageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class StorageLineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = StorageLine.objects.all()
    serializer_class = StorageLineSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer







