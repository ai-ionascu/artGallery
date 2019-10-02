from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from profiles.forms import UserLoginForm, RegistrationForm, EditUserForm, EditProfileForm, PaymentForm
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe

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
                messages.success(request,'You have been successfully logged in.')
                return redirect(reverse('index'))

            else:
                login_form.add_error(None, 'Username or password is incorrect.')

    else:
        login_form=UserLoginForm()

    return render(request, 'login.html', {'login_form': login_form})

def register_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('index'))

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)

        if reg_form.is_valid():
            
            try:
                      
                customer = stripe.Customer.create(
                                            name ='{} {}'.format(reg_form.cleaned_data.get('first_name'),
                                                                reg_form.cleaned_data.get('last_name')),
                                            email=str(reg_form.cleaned_data.get('email')),
                                            source=str(reg_form.cleaned_data.get('token')) # obtained with Stripe.js
                                            )

                stripe.Subscription.create(
                                            customer=customer.id,
                                            items=[
                                                        {
                                                        'plan': 'M01',
                                                        },
                                                    ],
                                                    )
                user = reg_form.save() 
                user.profile.profile_type = reg_form.cleaned_data.get('profile_type')
                user.profile.phone = reg_form.cleaned_data.get('phone')
                user.profile.address_line1 = reg_form.cleaned_data.get('address_line1')
                user.profile.address_line2 = reg_form.cleaned_data.get('address_line2')
                user.profile.city = reg_form.cleaned_data.get('city')
                user.profile.county = reg_form.cleaned_data.get('county')
                user.profile.country = reg_form.cleaned_data.get('country')
                user.profile.zip_code = reg_form.cleaned_data.get('zip_code')
                user.save()

            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

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

    return render(request, 'register.html', {'reg_form': reg_form, 'publishable' : settings.STRIPE_PUBLISHABLE})

def edit_profile_view(request):
    
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