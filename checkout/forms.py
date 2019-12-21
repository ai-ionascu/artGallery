from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email_address', 'phone_number', 'address_line1', 'address_line2', 'city', 'county', 'country', 'zip_code')