from django.contrib import admin
from .models import Profile, AddressMixin

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):

    fields = ('user','profile_type', 'phone', 'address_line1','address_line2', 'city', 'county', 'country', 'zip_code')

admin.site.register(Profile, ProfileAdmin)