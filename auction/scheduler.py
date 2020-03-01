def declare_winner(auction):
    if auction.bid_set.all():
        auction.winner = auction.bid_set.order_by('-bid')[0].bidder
        auction.winner_price = auction.bid_set.order_by('-bid')[0].bid
        auction.save(update_fields=['winner', 'winner_price'])
        print('I have declared the winner.')
    else:
        print('There are no bids.')