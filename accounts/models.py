from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from cart.models import CartItem
# Create your models here.
class User(AbstractBaseUser):
    admin_request_choiche=(
        ('requested', 'Requested'),
        ('approved', 'Approved'),
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    admin_request=models.CharField(max_length=255, null=True, blank=True, choices=admin_request_choiche)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_image = models.ImageField(blank=True, null=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender'] 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def wishlist_count(self):
        return self.user_wishlist.count()
    
    def cart_count(self):
        cart_item = CartItem.objects.filter(cart__user=self)
        cart_item_count = 0
        for item in cart_item:
            cart_item_count += item.quantity
        return cart_item_count
    
    def cart_item(self):
        return CartItem.objects.filter(cart__user=self)
    
    def calculate_subtotal(self):
        cart_item = CartItem.objects.filter(cart__user=self)
        sub_total = 0
        for item in cart_item:
            sub_total += item.subtotal
        return sub_total