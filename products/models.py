from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1. Categories"

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    
    def __str__(self):
        return self.name + '--' + self.category.name
    
    class Meta:
        verbose_name_plural = "2. Sub Categories"

# Product Model 
class Product(models.Model):
    product_name  = models.CharField(max_length=100)
    product_image  = models.ImageField(upload_to='product')
    product_brand  = models.CharField(max_length=100, default="No Brand")
    product_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    product_slug = models.SlugField(unique=True, null=True, blank=True)
    product_price = models.IntegerField()
    product_description = models.TextField()
    product_quantity = models.IntegerField(null=True)
    product_sold_quantity = models.IntegerField(null=True)
    product_location = models.CharField(max_length=100)
    product_warrenty = models.BooleanField(default=False)
    product_cash_payment = models.BooleanField(default=False)
    product_online_payment = models.BooleanField(default=False)
    product_return = models.BooleanField(default=False)
    product_added_date = models.DateTimeField(auto_now_add=True, null=True)
    product_stock_data = models.DateTimeField(auto_now=True, null=True)  

    def str(self) -> str:
        return self.product_name
    
    class Meta:
        verbose_name_plural ="3. Products"
        ordering = ['-product_added_date']
        

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





