from django.db import models
from accounts.models import User

# Create your models here.

class Blog(models.Model):
    blog_image = models.ImageField(upload_to='blog')
    blog_title = models.CharField(max_length=255)
    blog_text = models.TextField(max_length=10000)
    blog_date = models.DateField(auto_now_add=True)
    blog_writer = models.CharField(max_length=255, null=True)
    blog_topic = models.CharField(max_length=255, null=True)
 
    
    

class Blog_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)
    comment_date = models.DateField(auto_now_add=True)
    
    