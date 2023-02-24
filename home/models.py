from django.db import models

# Create your models here.


class AlertNews(models.Model):
    alertNews= models.CharField(max_length=200)
    alertNewsSubtitle = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(AlertNews, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.alertNews