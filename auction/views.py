from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import utc
from .models import Auction, Bid
from paintings.models import Painting
from .forms import AuctionForm, BidForm
import datetime
from django.core.exceptions import ValidationError
from .scheduler import declare_winner
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

@login_required
def start_auction_view(request):

    if request.POST:

        auction_form = AuctionForm(request.POST, request=request)
        if auction_form.is_valid():
            auction = auction_form.save(commit=False)
            auction.seller = request.user
            auction.start_date = datetime.datetime.utcnow().replace(tzinfo=utc)
            end_date = auction.start_date + auction.duration
            scheduler = BackgroundScheduler()
            scheduler.add_job(declare_winner, 'date', run_date=end_date, args=[request,auction])
            scheduler.start()
            auction.save()
            messages.success(request,'An auction for your painting has been successfully created.')
            return redirect(reverse('index'))
        else:
            messages.error(request,"We couldn't create an auction for this painting.")
    else:
        auction_form = AuctionForm(request=request)

    return render (request, 'start_auction.html', {'auction_form' : auction_form})

def list_auctions_view(request, id=None):

    context = {}
    auctions_list = Auction.objects.all()
    context['auctions'] = auctions_list
    context['id'] = id
    
    return render(request,  'auctions_list.html', context)

def detail_auction_view(request, id=None):
    auction = get_object_or_404(Auction, id=id)
    bid_form = BidForm(auction=auction)    
    return render(request, 'auction_detail.html', {'auction': auction, 'bid_form': bid_form, 'message': 'You have successfully placed a bid.'})

def place_bid(request, id=None):
    auction = get_object_or_404(Auction, id=id)
    if request.is_ajax and request.POST:
        bid_form = BidForm(request.POST, auction=auction)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.bidder = request.user
            bid.auction = auction
            bid.save()
            current_price = bid.auction.current_price

            ser_bid = serializers.serialize('json', [bid, ])
            return JsonResponse({'bid': ser_bid, 'current_price':current_price}, status=200)
        else:
            return JsonResponse({"error": bid_form.errors}, status=400)
        return JsonResponse({"error": "error"}, status=400)