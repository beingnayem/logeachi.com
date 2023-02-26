from django.shortcuts import render
from products.models import Product, Category
from home.models import AlertNews , BannerSlider

# Create your views here.

def index(request,):

    context = {'products': Product.objects.all(), 'categories': Category.objects.all(), 'Alert_news': AlertNews.objects.all(), 'sliders':BannerSlider.objects.all()}
    
    return render(request, 'home/index.html' , context)
