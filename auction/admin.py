from django.contrib import admin
from .models import Bid, Auction

# Register your models here.

admin.site.register(Auction)
admin.site.register(Bid)