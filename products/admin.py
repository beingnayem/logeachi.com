# from django.contrib import admin

# # Register your models here.
# from . models import *

# admin.site.register(Category)

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display=['pk','product_name', 'category', 'added_date', 'price', 'quantity', 'image']

# @admin.register(Cart)
# class CartAdminModel(admin.ModelAdmin):
#     list_display=['pk', 'user', 'product', 'quantity']

# @admin.register(Wishlist)
# class WishlistAdminModel(admin.ModelAdmin):
#     list_display=['pk', 'user', 'product']

# class OrderItemInline(admin.TabularInline):
#     model = OrderLineItem

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'customer', 'order_date', 'total_cost', 'shipping_address')
#     inlines = [OrderItemInline]

# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'order', 'product', 'quantity', 'cost')

#     def cost(self, obj):
#         return obj.quantity * obj.product.price

# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderLineItem, OrderItemAdmin)