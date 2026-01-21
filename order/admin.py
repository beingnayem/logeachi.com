from django.contrib import admin
from .models import Order, OrderItem, PaymentGateWaySettings, Payment

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_status']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'subtotal'] 

@admin.register(PaymentGateWaySettings)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['id', 'store_id']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'payment_amount', 'payment_method', 'payment_status']