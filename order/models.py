from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from cart.models import CartItem
from customer.models import Address
from products.models import Product
from django.utils.crypto import get_random_string

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('case_on_delivery', 'Cash on Delivery'),
        ('paypal', 'PayPal'),
        ('sslcommerz', 'SSLCOMMERZ'),
    )

    order_id = models.CharField(
        max_length=10, 
        unique=True, 
        default=get_random_string(length=10), 
        editable=False, 
        primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(
        Address,
        related_name='billing_orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    shipping_address = models.ForeignKey(
        Address,
        related_name='shipping_orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=(('unpaid', 'Unpaid'), ('paid', 'Paid')),
        default='unpaid'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='credit_card'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        order_items = self.order_items.all()
        total = sum(item.subtotal for item in order_items)
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        # Calculate subtotal before saving
        self.subtotal = self.product.product_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"
