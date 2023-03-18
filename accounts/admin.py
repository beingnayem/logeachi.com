from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class  UserModelAdmin(admin.ModelAdmin):
    list_display=['pk', 'first_name', 'email']


@admin.register(Address)
class  AddressModelAdmin(admin.ModelAdmin):
    list_display=[
        'pk', 'full_name', 'customer', 'phone', 'city', 'thana', 'postal_code', 'detail_address' 
        ]

