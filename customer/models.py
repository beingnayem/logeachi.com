from django.db import models
from accounts.models import *
# Create your models here.

class Address(models.Model):
    COUNTRY_CHOICES = (
        ('Bangladesh', 'Bangladesh'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='Bangladesh')
    zila = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    details_address = models.CharField(max_length=255)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)
    phone_number =  models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        return f'{self.country}, {self.zila}, {self.thana}, {self.postal_code}'