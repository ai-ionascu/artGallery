from django.db import models
from django.contrib.auth.models import User
from paintings.models import Painting
from django.core.exceptions import ValidationError
import datetime
from .scheduler import declare_winner
from apscheduler.schedulers.background import BackgroundScheduler

# Create your models here.

class Auction(models.Model):
    seller = models.ForeignKey(User, related_name='Seller')
    painting = models.ForeignKey(Painting)
    start_price = models.IntegerField()
    increment = models.IntegerField()

    @property
    def current_price(self):
    
        count = self.bid_set.count()
        price = self.start_price
        if count ==0:
            price=price
        elif count == 1:
            price += self.increment
        else:
            bid_delta = self.bid_set.order_by('-bid')[0].bid - self.bid_set.order_by('-bid')[1].bid
            factor = bid_delta // self.increment
            if factor > 1:
                price = self.bid_set.order_by('-bid')[1].bid + self.increment
            elif factor == 1:
                if bid_delta % self.increment == 0:
                    price = self.bid_set.order_by('-bid')[0].bid
                else:
                    price = self.bid_set.order_by('-bid')[1].bid + self.increment
            else:
                price = self.bid_set.order_by('-bid')[1].bid
        return price

    @property
    def time_left(self):

        start_date = self.start_date
        end_date = start_date + self.duration
        time_left = end_date - datetime.datetime.now(datetime.timezone.utc)
        while end_date >= datetime.datetime.now(datetime.timezone.utc):
            total_seconds = int(time_left.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = ((total_seconds % 86400) % 3600) // 60
            seconds = ((total_seconds % 86400) % 3600) % 60

            return '{} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds)

    winner_price = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(User, related_name='Winner', blank=True, null=True)
    start_date = models.DateTimeField()
    duration = models.DurationField()

    @property
    def is_active(self):
        end_date = self.start_date + self.duration
        return end_date >= datetime.datetime.now(datetime.timezone.utc)
    
    def __str__(self):
        return "%s sold by %s" %(self.painting, self.seller)

    def save(self, *args, **kwargs):
        if self._state.adding == True:
            end_date = self.start_date + self.duration
            scheduler = BackgroundScheduler()
            scheduler.add_job(declare_winner, 'date', run_date=end_date, args=[self])
            scheduler.start()
        super().save(*args, **kwargs)

class Bid(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name="bidder", blank=True, null=True)
    bid = models.IntegerField()

    def __str__(self):
        return "%s, bid ammount %s, for the auction: %s" %(self.bidder, self.bid, self.auction)
    