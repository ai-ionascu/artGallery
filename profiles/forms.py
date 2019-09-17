from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm

# Create your forms here.

class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)
    PROFILE_CHOICES = (('ARTIST', 'Artist'), ('CUSTOMER', 'Customer'))
    profile_type = forms.ChoiceField(choices=PROFILE_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(max_length=24, required=False)
    address_line1 = forms.CharField(max_length=128, required=False)
    address_line2 = forms.CharField(max_length=128, required=False)
    city = forms.CharField(max_length=64, required=False)
    county = forms.CharField(max_length=64, required=False)
    country = forms.CharField(max_length=64, required=False)
    zip_code = forms.CharField(max_length=8, required=False)

    class Meta:
        model = User
        fields = ('profile_type', 'username','first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user    