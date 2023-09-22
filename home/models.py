from django.db import models
from products.models import Category, Subcategory
from datetime import datetime, timedelta
from accounts.models import User

# Create your models here.

class Home_Slider(models.Model):
    slider_banner = models.ImageField(upload_to='slider')
    slider_offer_title = models.CharField(max_length=155)
    slider_offer = models.CharField(max_length=155)
    slider_offer_description = models.CharField(max_length=155)
    slider_offer_starting_price = models.DecimalField(max_digits=15, decimal_places=2)

class Newsletter(models.Model):
    GenderChoiche=(
        ('male','Male'),
        ('female','Female'),
    )
    email= models.EmailField(max_length=155)
    gender = models.CharField(max_length=10, choices=GenderChoiche, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.email


class Queries(models.Model):
    QueryChoiche=(
        ('recived','Recived'),
        ('replyed','Replyed'),
    )
    name = models.CharField(max_length=155)
    email= models.EmailField(max_length=155)
    subject= models.CharField(max_length=255)
    query_message= models.TextField(max_length=1000)
    query_date = models.DateTimeField(auto_now_add=True)
    query_status = models.CharField(max_length=10, choices=QueryChoiche, default='recived')
    reply_date = models.DateTimeField(auto_now=True)
    query_reply= models.TextField(max_length=1000, null=True, blank=True, default=None)
    
    def __str__(self) -> str:
        return self.name

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='Banner')
    banner_title = models.CharField(max_length=155)
    banner_offer = models.CharField(max_length=155)
    banner_product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='banner_product_category')


class Event(models.Model):
    event_banner = models.ImageField(upload_to='Event')
    event_title = models.CharField(max_length=155)
    event_offer_title = models.CharField(max_length=155)
    event_offer = models.CharField(max_length=155)
    event_product_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='event_product_category')
    event_deadline = models.DateTimeField(blank=True, null=True)
    
    
    def formatted_deadline(self):
        # Check if event_deadline is not None
        if self.event_deadline:
            return self.event_deadline.strftime('%Y/%m/%d')
        else:
            return None
        
    def is_event_over(self):
        if self.event_deadline:
            # Get the current date
            current_date = datetime.now().date()
            
            # Check if the current date is after the event deadline
            return current_date > self.event_deadline.date()
        else:
            return False  # Return False if the event date is not set
        
        
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_by')
    feedback = models.TextField(max_length=300)
    feedback_date = models.DateTimeField(auto_now_add=True)
    is_display = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name
