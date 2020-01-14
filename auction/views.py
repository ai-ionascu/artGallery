from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Auction
from paintings.models import Painting
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
            messages.success(request,'An auction for your painting has been successfully created.')
            return redirect(reverse('index'))
        else:
            messages.error(request,"We couldn't create an auction for this painting.")
    else:
        auction_form = AuctionForm(request=request)

    return render (request, 'start_auction.html', {'auction_form' : auction_form})

def list_auctions_view(request, seller=None):

    auctions_list = Auction.objects.all()

    if request.user.is_authenticated() and seller == request.user:
        own_auctions_list = Auction.objects.filter(seller=request.user)
        return render(request,  'auctions_list.html', {'own_auctions': own_auctions_list, 'seller': seller})

    return render(request,  'auctions_list.html', {'auctions': auctions_list, 'seller': seller})

def detail_auction_view(request, id=None):
    auction = get_object_or_404(Auction, id=id)
    return render(request, 'auction_detail.html', {'auction': auction})