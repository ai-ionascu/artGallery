from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):

    name = models.CharField(max_length=128, blank=True, default='')
    bio = models.TextField(default='')
    born_year = models.IntegerField()
    deceased_year = models.IntegerField()

    def __str__(self):
        return self.name

class Subject(models.Model):

    subject = models.CharField(max_length=128, blank=True, default='')

    def __str__(self):
        return self.subject

class Trend(models.Model):

    trend = models.CharField(max_length=128, blank=True, default='')

    def __str__(self):
        return self.trend

class Media(models.Model):

    media = models.CharField(max_length=128, blank=True, default='')
    
    def __str__(self):
        return self.media

class Painting(models.Model):
    name = models.CharField(max_length=128, default='') 
    artist = models.ForeignKey(Artist, blank=True, null=True)
    artist_user = models.ForeignKey(User, blank=True, null=True)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    subject = models.ManyToManyField(Subject, blank=True)
    trend = models.ForeignKey(Trend, blank=True, null=True)
    media = models.ForeignKey(Media, blank=True, null=True)
    year = models.IntegerField()
    SIZE_CHOICES = (('SMALL', 'Small'), ('SMALL', 'Medium'), ('SMALL', 'Large'))
    size = models.CharField(max_length=24, choices=SIZE_CHOICES, blank=True, default='')
    price = models.DecimalField(max_digits=24, decimal_places=2)
    availability = models.BooleanField()
    def __str__(self):
        return self.name