from django.conf.urls import url
from checkout.views import checkout

urlpatterns = [
    url(r'^$', checkout, name='checkout'),
    url(r'^(?P<auction_id>\d+)$', checkout, name='checkout'),
    ]