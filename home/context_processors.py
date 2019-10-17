from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import stripe
from paintings.models import Subject, Trend, Media, Painting

def subscription_to_context(request):

    context={}
    if request.user.is_authenticated:
        if request.user.profile.profile_type == 'ARTIST':
            subscription = stripe.Subscription.retrieve(request.user.profile.subscr_id)
            context = {'subscription' : subscription.cancel_at_period_end}

    return context

def navbar(request):
    size = Painting._meta.get_field('size').choices
    print(size)
    return {'subject': Subject.objects.order_by("-id")[:5], 
            'trend': Trend.objects.order_by("-id")[:5],
            'media': Media.objects.order_by("-id")[:5],
            'size':size}