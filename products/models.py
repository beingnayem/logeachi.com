from django.db import models
from accounts.models import User
# Create your models here.

from django.utils.text import slugify



class Category(models.Model):
    
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='product', null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.category_name


class Product(models.Model):

    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.IntegerField()
    product_description = models.TextField()
    quantity = models.IntegerField(null=True)

    class Meta:
        ordering = ['-added_date']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.product_name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.price
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)