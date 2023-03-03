from django.db import models

# Create your models here.

<<<<<<< HEAD
=======

>>>>>>> 8258119982bf0986f3488cc85de52e95f97944f0
    
class BannerSlider(models.Model):
    banner_img=models.ImageField(upload_to='banner')
    banner_title=models.CharField(max_length=200)
    banner_subtitle=models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(BannerSlider, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.banner_title

