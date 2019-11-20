from django.db import models
from home.models import OwnerMixin

# Create your models here.

class Artist(OwnerMixin, models.Model):

    artist = models.CharField(max_length=128, blank=False, null=False)
    image = models.ImageField(upload_to='images', default='/default/default_img.jpg')
    bio = models.TextField(blank=True)
    born_year = models.IntegerField(null=True)
    deceased_year = models.IntegerField(null=True)

    def __str__(self):
        return self.artist