from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from artists.models import Artist
from home.models import OwnerMixin

# Create your models here.

class Subject(OwnerMixin, models.Model):

    subject = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.subject

class Trend(OwnerMixin, models.Model):

    trend = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.trend

class Media(OwnerMixin, models.Model):

    media = models.CharField(max_length=128, default='')
    
    def __str__(self):
        return self.media

class Painting(OwnerMixin, models.Model):
    name = models.CharField(max_length=128, default='') 
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    subject = models.ManyToManyField(Subject) 
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    year = models.IntegerField()
    SIZE_CHOICES = (('', '---------'), ('SMALL', 'Small'), ('MEDIUM', 'Medium'), ('LARGE', 'Large'))
    size = models.CharField(max_length=24, choices=SIZE_CHOICES, default='')
    price = models.IntegerField()
    availability = models.BooleanField()

    def __str__(self):
        return self.name

    def get_subject_values(self):
        result = []

        for subj in self.subject.all():
            result.append(subj.subject)

        return result

class Comment(models.Model):

    painting = models.ForeignKey(Painting, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='users_comments')
    comment = models.TextField(max_length=400, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.comment)[:30]

class Like(models.Model):

    painting = models.OneToOneField(Painting, related_name='likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='users_likes')

    def __str__(self):
        return self.painting.name