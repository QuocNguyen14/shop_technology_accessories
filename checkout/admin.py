from django.contrib import admin
from .models import DeliveryOptions

admin.site.register(DeliveryOptions)

from checkout.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'postal_code')
