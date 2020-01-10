from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AuctionForm
import datetime

# Create your views here.

@login_required
def start_auction_view(request):

    if request.POST:

        auction_form = AuctionForm(request.POST, request=request)
        if auction_form.is_valid():
            auction = auction_form.save(commit=False)
            auction.seller = request.user
            auction.start_date = datetime.datetime.now()
            auction.save()

    else:

        auction_form = AuctionForm(request=request)

    return render (request, 'start_auction.html', {'auction_form' : auction_form})
