from django.contrib import admin
from customer.models import *
# Register your models here.


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'zila',
        'thana',
        'postal_code',
        'is_default_shipping',
        'is_default_billing',
        'phone_number'
    ]