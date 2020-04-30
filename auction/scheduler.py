from django.core.mail import EmailMessage
from django.template import loader
from django.conf import settings

def send_email(request, auction):

    subject = 'Auction Finished'
    from_email = settings.EMAIL_HOST_USER
    to = [auction.winner.email,]
    context = {}
    context['auction'] = auction
    html_content = loader.render_to_string('mail_confirmation.html', context, request=request)
    message = EmailMessage(subject, html_content, from_email, to)
    message.send()


def declare_winner(request, auction):
    if auction.bid_set.all():
        highest_bid = auction.bid_set.order_by('-bid')[0]
        if highest_bid.bid >= auction.min_price:
            auction.winner = highest_bid.bidder
            auction.winner_price = auction.current_price if auction.current_price >=auction.min_price else highest_bid.bid
            auction.save(update_fields=['winner', 'winner_price'])
            print('I have declared the winner.')
            send_email(request, auction)
            print('email sent')
        else:
            print('The minimum price has not been reached.')
    else:
        print('There are no bids.')