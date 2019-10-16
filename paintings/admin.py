from django.contrib import admin
from .models import Artist, Subject, Trend, Painting, Media
from django.utils.html import format_html

# # Register your models here.

class PaintingAdmin(admin.ModelAdmin):  
    
    def image_tag(self, obj):
        return format_html('<img src="{}" alt="{}" max-width="300" height="150"/>'.format(obj.image.url, obj.name))

    image_tag.short_description = 'Image Preview'

    fields = ( 'name', 'artist', 'artist_user', 'image',
             'image_tag', 'description', 'year', 'trend', 
             'subject', 'media', 'size', 'price', 'availability' )
    readonly_fields = ('image_tag', )
    list_display = ['name', 'artist', 'image_tag', ]

admin.site.register(Painting, PaintingAdmin)