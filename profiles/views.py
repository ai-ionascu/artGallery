from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from profiles.forms import UserLoginForm, RegistrationForm, EditUserForm, EditProfileForm
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe
import datetime

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.

def index_view(request):
    # returns the gallery homepage
    
    return render(request, 'index.html')


@login_required
def logout_view(request):
    # logs the user out

    auth.logout(request)
    messages.success(request, 'You have been successfully logged out.')

    return redirect(reverse('index'))


def login_view(request):

    # checks if the user exist
    # if it does exist, the user is authenticated

    if request.user.is_authenticated():
        return redirect(reverse('index'))

    if request.method == 'POST':

        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():

            user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])

            if user:

                auth.login(user=user,request=request)
                if user.profile.profile_type == 'ARTIST':
                    subscription = stripe.Subscription.retrieve(request.user.profile.subscr_id)
                    if subscription.cancel_at_period_end == True:
                        if subscription.current_period_end < datetime.datetime.now().timestamp():
                            User.objects.get(username=request.POST['username']).delete()
                            messages.error(request,'Your subscription has been cancelled. Account permanently deleted, please proceed to registration page.')
                            return redirect(reverse('index'))
                        else:
                            delta = datetime.datetime.fromtimestamp(int(subscription.current_period_end))-datetime.datetime.now()
                            if delta.days < 30:
                                messages.error(request,'Your subscription will be ended in {} days.'.format(delta.days))

                messages.success(request,'You have been successfully logged in.')
                return redirect(reverse('index'))

            else:
                login_form.add_error(None, 'Username or password is incorrect.')

    else:
        login_form=UserLoginForm()

    return render(request, 'login.html', {'login_form': login_form})

def registration_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('index'))
    
    types = Profile._meta.get_field('profile_type').choices

    if request.method == 'POST':
        request.session['profile_type'] = request.POST['profile_type']
        return redirect(reverse('new_profile'))
    
    return render(request, 'register.html', { 'types':types })

def new_profile_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('index'))
    
    profile_type = request.session.get('profile_type')

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)

        if reg_form.is_valid():

            if profile_type == 'ARTIST':

                try:
                      
                    customer = stripe.Customer.create(
                                                name ='{} {}'.format(reg_form.cleaned_data.get('first_name'),
                                                                    reg_form.cleaned_data.get('last_name')),
                                                email=str(reg_form.cleaned_data.get('email')),
                                                source=str(reg_form.cleaned_data.get('token')) # obtained with Stripe.js
                                                )

                    subscription = stripe.Subscription.create(
                                                customer=customer.id,
                                                items=[
                                                            {
                                                            'plan': request.POST['plan'],
                                                            },
                                                        ],
                                                        )
                    user = reg_form.save()
                    user.profile.stripe_id = customer.id
                    user.profile.subscr_id = subscription.id
                    

                except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")

            else:
                user = reg_form.save()
                
            user.profile.profile_type = request.POST.get('profile_type')
            user.profile.phone = reg_form.cleaned_data.get('phone')
            user.profile.address_line1 = reg_form.cleaned_data.get('address_line1')
            user.profile.address_line2 = reg_form.cleaned_data.get('address_line2')
            user.profile.city = reg_form.cleaned_data.get('city')
            user.profile.county = reg_form.cleaned_data.get('county')
            user.profile.country = reg_form.cleaned_data.get('country')
            user.profile.zip_code = reg_form.cleaned_data.get('zip_code')
            user.save()

            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])

            if user:
                auth.login(request=request, user=user)
                messages.success(request,'You have been successfully registered.')

            else:
                messages.error(request, 'Registration failed, please try again later.')

            return redirect(reverse('index'))

    else:
        reg_form = RegistrationForm()

    return render(request, 'new_profile.html', {'reg_form': reg_form, 'profile_type':profile_type, 'publishable': settings.STRIPE_PUBLISHABLE})

def edit_profile_view(request,id=None):
    
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance=request.user)
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if edit_user_form.is_valid and edit_profile_form.is_valid:
            user_info = edit_user_form.save()
            profile_info = edit_profile_form.save(commit=False)
            profile_info.user = user_info
            profile_info.save()
            messages.success(request,'Your profile has been successfully updated.')
            return redirect(reverse('index'))

    else:
        edit_user_form = EditUserForm(instance=request.user)
        edit_profile_form = EditProfileForm(instance=request.user.profile)

    
    return render(request, 'edit_profile.html', {'edit_user_form': edit_user_form, 'edit_profile_form': edit_profile_form})

@receiver(post_save, sender=User)
def create_user_and_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@login_required
def unsubscribe_view(request):
    
    try:
        # customer = stripe.Customer.retrieve(request.user.profile.stripe_id)
        subscription = stripe.Subscription.retrieve(request.user.profile.subscr_id)
        end_date_ts = subscription.current_period_end
        end_date = datetime.datetime.fromtimestamp(int(end_date_ts))
        stripe.Subscription.modify(request.user.profile.subscr_id, cancel_at_period_end=True)
        messages.success(request, 'You subscription has been successfully cancelled. Your account will be permanently deleted at {}'.format(end_date))

    except Exception :

        messages.error(request, "An error occured, we couldn't cancel your subscription.")
    

    return redirect(reverse('index'))

@login_required
def reactivate_subscription_view(request):

    try:
        stripe.Subscription.retrieve(request.user.profile.subscr_id)
        stripe.Subscription.modify(request.user.profile.subscr_id, cancel_at_period_end=False)
        messages.success(request, 'You subscription has been successfully reactivated')

    except Exception :

        messages.error(request, "An error occured, we couldn't reactivate your subscription.")
    

    return redirect(reverse('index'))

@login_required
def delete_user_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            del_user = User.objects.get(username=form.cleaned_data['username'])
            if del_user.profile.profile_type == 'ARTIST':
                stripe.Subscription.retrieve(request.user.profile.subscr_id)
                stripe.Subscription.delete(request.user.profile.subscr_id)
                messages.success(request, 'You subscription has been cancelled.')
            if del_user is not None:
                del_user.delete()
                messages.success(request, "We have successfully deleted your account.")
                return redirect(reverse('index'))
                

        else:
            messages.error(request, "We could not delete your account.")
    else:
        form = EditUserForm(instance=request.user)
        
    return render(request, 'delete_profile.html', {'form':form})