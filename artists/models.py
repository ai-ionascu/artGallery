from django.db import models

# Create your models here.

class Artist(models.Model):

    name = models.CharField(max_length=128, blank=False, null=False)
    image = models.ImageField(upload_to='images', default='/default/default_img.jpg')
    bio = models.TextField(blank=True)
    born_year = models.IntegerField(blank=True)
    deceased_year = models.IntegerField(blank=True)

    def __str__(self):
        return self.name