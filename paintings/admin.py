from django.contrib import admin
from .models import Painting, Subject, Trend, Media, Comment, Like
from django.utils.html import format_html
from django.contrib.admin.sites import AlreadyRegistered

# # Register your models here.

class SubjectInline(admin.TabularInline):
    model = Painting.subject.through
    extra = 1

class PaintingAdmin(admin.ModelAdmin):  

    inlines = [SubjectInline]
    
    def image_tag(self, obj):
        
        if obj.image:
            return format_html('<img src="{}" alt="{}" max-width="200" height="100"/>'.format(obj.image.url, obj.name))

    image_tag.short_description = 'Image Preview'

    fields = ( 'name', 'artist', 'owner', 'image',
             'image_tag', 'description', 'subject', 'trend', 'media', 'year', 'size', 'price', 'availability' )
    readonly_fields = ('image_tag', )
    list_display = ['name', 'artist', 'image_tag', 'owner', ]

admin.site.register(Painting, PaintingAdmin)

for m in [Subject, Trend, Media]:
    class m_admin(admin.ModelAdmin): 
        def rename(self):
            self.__name__ = '{}Admin'.format(m)
            return self 
        model = m
        def get_model_perms(self, request):
            return {}

    try:
        admin.site.register(m, m_admin)
    except AlreadyRegistered:
        pass 
      
admin.site.register(Comment)
admin.site.register(Like)