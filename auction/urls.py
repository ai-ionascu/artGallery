from django.conf.urls import url, include
from auction.views import start_auction_view


urlpatterns = [
    # url(r'^$', list_auctions_view, name='auctions'),
    url( r'^start/$', start_auction_view, name='start_auction'),

]