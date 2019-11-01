from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):

    name = models.CharField(max_length=128, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    born_year = models.IntegerField(blank=True, null=True, default=False)
    deceased_year = models.IntegerField(blank=True, null=True, default=False)

    def __str__(self):
        return self.name

class Subject(models.Model):

    subject = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.subject

class Trend(models.Model):

    trend = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.trend

class Media(models.Model):

    media = models.CharField(max_length=128, default='')
    
    def __str__(self):
        return self.media

class Painting(models.Model):
    name = models.CharField(max_length=128, default='') 
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artist_user = models.ForeignKey(User)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    subject = models.ManyToManyField(Subject) 
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    year = models.IntegerField()
    SIZE_CHOICES = (('', '---------'), ('SMALL', 'Small'), ('SMALL', 'Medium'), ('SMALL', 'Large'))
    size = models.CharField(max_length=24, choices=SIZE_CHOICES, default='')
    price = models.DecimalField(max_digits=24, decimal_places=2)
    availability = models.BooleanField()

    def __str__(self):
        return self.name

    def get_subject_values(self):
        result = []

        for subj in self.subject.all():
            result.append(subj.subject)

        return result