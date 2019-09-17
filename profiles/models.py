from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class AddressMixin(models.Model):

    class Meta:
        abstract = True
    
    address_line1 = models.CharField(max_length=128, blank=True, default='')
    address_line2 = models.CharField(max_length=128, blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    county = models.CharField(max_length=64, blank=True, default='')
    country = models.CharField(max_length=64, blank=True, default='')
    zip_code = models.CharField(max_length=8, blank=True, default='')

class Profile(AddressMixin, models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PROFILE_CHOICES = (('ARTIST', 'Artist'), ('CUSTOMER', 'Customer'))
    profile_type = models.CharField(max_length=24, choices=PROFILE_CHOICES, blank=False, default='')
    phone = models.CharField(max_length=24, null=False, blank=True, default='')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_and_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
   