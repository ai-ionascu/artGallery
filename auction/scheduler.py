from urllib import request
from cart.views import add_to_cart

def declare_winner(auction):
    if auction.bid_set.all():
        auction.winner = auction.bid_set.order_by('-bid')[0].bidder
        auction.winner_price = auction.bid_set.order_by('-bid')[0].bid
        auction.save(update_fields=['winner', 'winner_price'])
        add_to_cart(request, auction.painting.id)
        print('I have declared the winner.')
    else:
        print('There are no bids.')