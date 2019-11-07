from django.contrib import admin
from .models import Artist
from django.utils.html import format_html

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):  
    
    def image_tag(self, obj):
        
        if obj.image:
            return format_html('<img src="{}" alt="{}" max-width="200" height="100"/>'.format(obj.image.url, obj.name))

    image_tag.short_description = 'Image Preview'

    fields = ( 'name', 'image', 'bio', 'born_year', 'deceased_year' )
    readonly_fields = ('image_tag', )
    list_display = ['name', 'image_tag', ]

admin.site.register(Artist, ArtistAdmin)