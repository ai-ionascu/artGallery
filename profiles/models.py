from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User)
    PROFILE_CHOICES = (('ARTIST', 'Artist'), ('CUSTOMER', 'Customer'))
    profile_type = models.CharField(max_length=24, choices=PROFILE_CHOICES, blank=False, default='')
    phone = models.CharField(max_length=24, null=False, blank=True, default='')

    def __str__(self):
        return self.user.username

class Address(models.Model):
    
    profile = models.OneToOneField(Profile)
    street1 = models.CharField(max_length=128, blank=True, default='')
    street2 = models.CharField(max_length=128, blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    county = models.CharField(max_length=64, blank=True, default='')
    country = models.CharField(max_length=64, blank=True, default='')
    zip_code = models.CharField(max_length=8, blank=True, default='')