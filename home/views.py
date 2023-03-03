from django.shortcuts import render
from products.models import Product, Category
from home.models import BannerSlider

# Create your views here.

def home(request):

    categoryID = request.GET.get('category')

    if categoryID:
        product = Product.objects.filter(category=categoryID)

    else:
        product = Product.objects.all()
    
    context = {'products': product, 'categories': Category.objects.all(), 'sliders':BannerSlider.objects.all(), }
    return render(request, 'home/index.html' , context)
