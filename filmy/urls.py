from django.conf.urls import patterns, url, include
from django.conf import settings

from filmy import settings
from filmy_app import views

from rest_framework.routers import DefaultRouter

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'video', views.VideoViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'audioinfo', views.AudioInfoViewSet)
router.register(r'videoinfo', views.VideoInfoViewSet)
router.register(r'storage', views.StorageViewSet)
router.register(r'storage_line', views.StorageLineViewSet)
router.register(r'device', views.DeviceViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'language', views.LanguageViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    #Home
    url(r'^$', views.HomeView.as_view(), name='home'),
    
    #API Rest Framework
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), )
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL, 'show_indexes': True}), )
