from django.db import models
from paintings.models import Painting

# Create your models here.

class ShippingAddressMixin(models.Model):

    class Meta:
        abstract = True
    
    address_line1 = models.CharField(max_length=128, blank=True, default='')
    address_line2 = models.CharField(max_length=128, blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    county = models.CharField(max_length=64, blank=True, default='')
    country = models.CharField(max_length=64, blank=True, default='')
    zip_code = models.CharField(max_length=8, blank=True, default='')

class Order(ShippingAddressMixin, models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email_address = models.EmailField(max_length=64, blank=False, default='')
    phone_number = models.CharField(max_length=20, blank=False)
    date = models.DateField()
    
    def __str__(self):
        return "{0}-{1}-{2} {3}".format(self.id, self.date, self.first_name, self.last_name)
        
        
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False)
    painting = models.ForeignKey(Painting, null=False)
    quantity = models.IntegerField(blank=False)
    
    def __str__(self):
        return "{0} {1} @ {2}".format(self.quantity, self.painting.name, self.painting.price)