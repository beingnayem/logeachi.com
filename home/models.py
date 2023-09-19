from django.db import models

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

