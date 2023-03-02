from django.shortcuts import render
from products.models import Product, Category
from home.models import AlertNews , BannerSlider

# Create your views here.

def home(request):
    
    # female_collection = Product.objects.filter(tergeted_buyer=       'Only Female')
    # male_collection = Product.objects.filter(tergeted_buyer = 'Only Male')
    # kids_collection = Product.objects.filter(tergeted_buyer = 'Only Kids')
    # both_collection = Product.objects.filter(tergeted_buyer = 'Male & Female')

    categoryID = request.GET.get('category')

    if categoryID:
        product = Product.objects.filter(category=categoryID)

    else:
        product = Product.objects.all()

    # context = {'cat_products':cat_products}
    
    # return render(request, 'products/category_products.html', context)
    
    context = {'products': product, 'categories': Category.objects.all(), 'Alert_news': AlertNews.objects.all(), 'sliders':BannerSlider.objects.all(), }
    
    return render(request, 'home/index.html' , context)
