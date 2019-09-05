from django.contrib import admin
from .models import Profile, Address

# Register your models here.

class AddressInline(admin.StackedInline):
    model = Address
    verbose_name = 'Address'
    verbose_name_plural = 'Address'
    
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
        ]

admin.site.register(Profile, ProfileAdmin)