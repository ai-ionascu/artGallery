from django.db import models
from django.contrib.auth.models import User
from paintings.models import Painting

# Create your models here.

class Auction(models.Model):
    seller = models.ForeignKey(User, related_name='Seller')
    painting = models.OneToOneField(Painting)
    start_price = models.DecimalField(max_digits=24, decimal_places=2)
    increment = models.DecimalField(max_digits=24, decimal_places=2)
    winner_price = models.DecimalField(max_digits=24, decimal_places=2, blank=True, null=True)
    winner = models.ForeignKey(User, related_name='Winner', blank=True, null=True)
    start_date = models.DateTimeField()

    DAYS_CHOICES = [(i, i) for i in range(1, 10+1)]
    # HOURS_CHOICES = [(i, i) for i in range(1, 24)]
    # MINUTES_CHOICES = [(i, i) for i in range(1, 60)]

    duration = models.DurationField()
    is_active = models.BooleanField()

class Bid(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.OneToOneField(User, null=True, blank=True)
    bid = models.DecimalField(max_digits=24, decimal_places=2) 