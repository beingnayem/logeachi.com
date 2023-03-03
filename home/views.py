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



def search(request):
    get_method =  request.GET.copy()
    key_words = get_method.get('keywords') or None
    product = Product.objects.all()
    product_list = []  # Initialize product_list to an empty list

    if key_words:
        key_word = get_method.get('keywords')
        product_list = product.filter(product_description__icontains=key_word)

    context= {'categories': Category.objects.all(),'products': product_list}

    return render(request, 'products/search-result.html', context)

