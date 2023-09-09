from django.contrib import admin
from .models import *
# # Register your models here.

@admin.register(MainCategory)
class MainCategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'main_category']
    
@admin.register(Subcategory)
class SubcategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'category'] 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('product_name',)}
    list_display = [
        'id', 
        'product_name', 
        'product_category', 
        'product_price', 
        'product_quantity'
    ]



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