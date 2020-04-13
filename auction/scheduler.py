def declare_winner(auction):
    if auction.bid_set.all():
        highest_bid = auction.bid_set.order_by('-bid')[0]
        if highest_bid.bid >= auction.min_price:
            auction.winner = highest_bid.bidder
            auction.winner_price = auction.current_price if auction.current_price >=auction.min_price else highest_bid.bid
            auction.save(update_fields=['winner', 'winner_price'])
            print('I have declared the winner.')
        else:
            print('The minimum price has not been reached.')
    else:
        print('There are no bids.')