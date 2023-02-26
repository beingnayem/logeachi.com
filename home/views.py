from django.shortcuts import render
from products.models import Product, Category
from home.models import AlertNews , BannerSlider

# Create your views here.

def index(request,):
    female_collection = Product.objects.filter(tergeted_buyer=       'Only Female')
    male_collection = Product.objects.filter(tergeted_buyer = 'Only Male')
    kids_collection = Product.objects.filter(tergeted_buyer = 'Only Kids')
    both_collection = Product.objects.filter(tergeted_buyer = 'Male & Female')
    
    context = {'products': Product.objects.all(), 'categories': Category.objects.all(), 'Alert_news': AlertNews.objects.all(), 'sliders':BannerSlider.objects.all(), 'female_collc': female_collection, 'male_collc': male_collection, 'kids_collc': kids_collection, 'both_collc': both_collection }
    
    return render(request, 'home/index.html' , context)
