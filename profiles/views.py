from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from profiles.forms import UserLoginForm

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
        reg_form = UserCreationForm(request.POST)

        if reg_form.is_valid():
            reg_form.save()
            messages.success(request,'You have been successfully registered.')

            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)

            return redirect(reverse('index'))

    else:
        reg_form = UserCreationForm()

    return render(request, 'register.html', {'reg_form': reg_form})
