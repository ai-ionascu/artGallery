from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from paintings.models import Painting
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):
    if request.method=="POST":
        order_form = OrderForm(request.POST)
        # payment_form = MakePaymentForm(request.POST)
        
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                painting = get_object_or_404(Painting, pk=id)
                total += quantity * painting.price
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
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('paintings'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        order_form = OrderForm()
        
    return render(request, "checkout.html", {'order_form': order_form, 'publishable': settings.STRIPE_PUBLISHABLE})