from django.contrib import admin
from .models import Artist, Subject, Trend, Painting, Media

# Register your models here.

admin.site.register(Artist)
admin.site.register(Subject)
admin.site.register(Trend)
admin.site.register(Painting)
admin.site.register(Media)