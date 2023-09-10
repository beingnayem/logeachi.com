from django.db import models

# Create your models here.

    
class Banner(models.Model):
    TypeChoice=(
    ('slider','Slider'),
    ('newslatter', 'Newslatter'), 
    ('promotion', 'Promotion'), 
    ('toster', 'Toster'),
    )
    banner_name=models.CharField(max_length=200)
    banner_type=models.CharField(max_length=200, choices=TypeChoice)
    banner_image=models.ImageField(upload_to='banner')
    

    def __str__(self) -> str:
        return self.banner_name

