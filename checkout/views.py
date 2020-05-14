from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import OrderLineItem
from auction.models import Auction
from django.conf import settings
from django.utils import timezone
from paintings.models import Painting
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request, auction_id=None):
    if auction_id:
        auction = get_object_or_404(Auction, id=auction_id)
        if 'cart' in request.session: request.session.pop('cart')
    else:
        auction = None
    if request.method=="POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            cart = request.session.get('cart', {})
            total = 0
            if auction_id: cart[auction.painting.id] = 1          
            for id, quantity in cart.items():
                painting = get_object_or_404(Painting, pk=id)
                price = auction.winner_price if auction else painting.price
                total += quantity * price
                order_line_item = OrderLineItem(
                    order = order, 
                    painting = painting, 
                    quantity = quantity
                    )
                order_line_item.save()
                
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "EUR",
                    description = request.user.email,
                    source=str(request.POST.get('token')), # obtained with Stripe.js
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                
            if customer.paid:
                messages.error(request, "You have successfully paid {}".format(customer.amount/100))
                request.session['cart'] = {}
                if auction:
                    return redirect(reverse('rate_seller', kwargs={'seller_id': auction.seller.id,'auction_id': auction.id}))
                return redirect(reverse('paintings'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        order_form = OrderForm()
        
    return render(request, "checkout.html", {'order_form': order_form, 'auction':auction, 'publishable': settings.STRIPE_PUBLISHABLE})

def rate_seller(request, seller_id= None, auction_id=None):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.user != auction.seller:
        return render(request, 'rate_seller.html', {'auction': auction})
    else:
        messages.error(request,'You should not rate yourself.')
        return(redirect(reverse('index')))