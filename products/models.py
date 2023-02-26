from django.db import models

# Create your models here.
# from base.models import BaseModel
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
    
    type=[
        ('Male & Female', 'Uni-sex'),
        ('Only Male',  'Male'),
        ('Only Female', 'Female'),
        ('Only Kids', 'Kids')
    ]

    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tergeted_buyer = models.CharField(max_length=50, choices=type, default='Uni-sex')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.IntegerField()
    product_description = models.TextField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.product_name

