from django.db import models
from accounts.models import User

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
    product_warrenty = models.BooleanField(null=True)
    product_cash_payment = models.BooleanField(null=True)
    product_online_payment = models.BooleanField(null=True)
    product_return = models.BooleanField(null=True)
    product_added_date = models.DateTimeField(auto_now_add=True, null=True)
    product_stock_date = models.DateTimeField(auto_now=True, null=True)  

    def str(self) -> str:
        return self.product_name
    
    class Meta:
        verbose_name_plural ="4. Products"
        ordering = ['-product_added_date']
        
        
class Product_Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    review = models.TextField(max_length=255)
    review_date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.product.product_name
    

    class Meta:
        verbose_name_plural ="5. ProductReview"

# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
#     shipping_cost = models.PositiveIntegerField(default=50)
#     order_date = models.DateTimeField(auto_now_add=True)
#     total_cost = models.PositiveIntegerField(default=0)

# class OrderLineItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)





