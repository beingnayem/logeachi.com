from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Category)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['pk','product_name', 'category', 'added_date', 'price', 'quantity', 'image']

@admin.register(Cart)
class CartAdminModel(admin.ModelAdmin):
    list_display=['pk', 'user', 'product', 'quantity']

@admin.register(Wishlist)
class WishlistAdminModel(admin.ModelAdmin):
    list_display=['pk', 'user', 'product']