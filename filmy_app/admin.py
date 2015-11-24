#Esto es para que en los videos aparezcan las lineas de almacenamiento en la parte de Administracion

from django.contrib import admin
from filmy_app.models import *

class StorageLineInline(admin.TabularInline):
    model = StorageLine

class VideoAdmin(admin.ModelAdmin):
    inlines = [
        StorageLineInline,
    ]

admin.site.register(Device)
admin.site.register(Storage)
admin.site.register(AudioInfo)
admin.site.register(VideoInfo)
admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Video,VideoAdmin)
