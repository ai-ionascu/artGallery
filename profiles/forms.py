from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profile

# Create your forms here.

class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)
    avatar = forms.ImageField(required=False)
    phone = forms.CharField(max_length=24, required=False)
    address_line1 = forms.CharField(max_length=128, required=False)
    address_line2 = forms.CharField(max_length=128, required=False)
    city = forms.CharField(max_length=64, required=False)
    county = forms.CharField(max_length=64, required=False)
    country = forms.CharField(max_length=64, required=False)
    zip_code = forms.CharField(max_length=8, required=False)
    token = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id':'token'}))

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique.')
        return email    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user    

class EditUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name')
            
class EditProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('avatar', 'phone', 'address_line1', 'address_line2', 'city', 'county', 'country', 'zip_code')