from django.db import models
from products.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlist')
    
class Cart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate subtotal before saving
        self.subtotal = self.product.product_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"

@receiver(pre_save, sender=CartItem)
def update_cart_item_subtotal(sender, instance, **kwargs):
    instance.subtotal = instance.product.product_price * instance.quantity
