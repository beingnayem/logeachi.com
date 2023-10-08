from django.db import models
from django.db.models import Avg
from django.utils import timezone
from datetime import date

class Main_Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = '1. Main Category'

class Category(models.Model):
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE, related_name='main_category', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "2. Categories"

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    
    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = "3. Sub Categories"

# Product Model 
class Product(models.Model):
    product_name  = models.CharField(max_length=100)
    product_image  = models.ImageField(upload_to='product')
    product_brand  = models.CharField(max_length=100, default="No Brand")
    product_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    product_slug = models.SlugField(unique=True, null=True, blank=True)
    product_price = models.DecimalField(max_digits=15, decimal_places=2)
    product_description = models.TextField()
    product_quantity = models.IntegerField(null=True)
    product_sold_quantity = models.IntegerField(default=0)
    product_location = models.CharField(max_length=100)
    product_featured = models.BooleanField(default=False)
    product_warrenty = models.BooleanField(null=True)
    product_cash_payment = models.BooleanField(null=True)
    product_online_payment = models.BooleanField(null=True)
    product_return = models.BooleanField(null=True)
    product_added_date = models.DateTimeField(auto_now_add=True, null=True)
    product_stock_date = models.DateTimeField(auto_now=True, null=True) 
    product_flash_expiry = models.DateField(null=True, blank=True) 
    

    def save(self, *args, **kwargs):
        # Use timezone.now() to ensure the datetime is timezone-aware
        if not self.product_added_date:
            self.product_added_date = timezone.now()
        self.product_stock_date = timezone.now()

        super().save(*args, **kwargs)

    def str(self) -> str:
        return self.product_name
    
    class Meta:
        verbose_name_plural ="4. Products"
        ordering = ['-product_added_date']
         
    def average_rating(self):
        # Calculate the average rating for the product
        return Product_Reviews_and_Rating.objects.filter(product=self).aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    def total_reviews(self):
        # Calculate the total number of reviews for the product
        return self.review_to.count()
    
    @classmethod
    def get_flash_products(cls):
        current_date = date.today()
        flash_products = cls.objects.filter(
            product_flash_expiry__gte=current_date
        )
        return flash_products
        
        
class Product_Reviews_and_Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_to')
    user =  models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='review_by')
    review = models.TextField(max_length=255)
    review_date = models.DateTimeField(auto_now_add=True, null=True)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.product.product_name
    

    class Meta:
        verbose_name_plural ="5. Product Review And Rating"
