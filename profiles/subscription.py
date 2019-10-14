from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import stripe

def subscription_to_context(request):

    if request.user.is_authenticated:
        subscription = stripe.Subscription.retrieve(request.user.profile.subscr_id)
        context = {'subscription' : subscription.cancel_at_period_end}
    else:
        context = {}

    return context