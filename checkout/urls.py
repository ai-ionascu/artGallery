from django.conf.urls import url
from checkout.views import checkout, rate_seller

urlpatterns = [
    url(r'^$', checkout, name='checkout'),
    url(r'^(?P<auction_id>\d+)$', checkout, name='checkout'),
    url( r'^auction/(?P<auction_id>\d+)/seller/(?P<seller_id>\d+)/rate$', rate_seller, name='rate_seller'),
    ]