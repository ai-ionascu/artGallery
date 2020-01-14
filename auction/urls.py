from django.conf.urls import url, include
from auction.views import list_auctions_view, start_auction_view, detail_auction_view


urlpatterns = [
    url(r'^$', list_auctions_view, name='auctions'),
    url(r'^user/(?P<seller>\d+)/$', list_auctions_view, name='my_auctions'),
    url( r'^start/$', start_auction_view, name='start_auction'),
    url( r'^(?P<id>\d+)/$', detail_auction_view, name='auction_detail'),

]