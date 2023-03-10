from django.shortcuts import render
from products.models import Product, Category
from home.models import BannerSlider

# Create your views here.

from django.core.paginator import Paginator
from django.shortcuts import render


def home(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 20)  # Show 20 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'sliders': BannerSlider.objects.all(),
    }
    return render(request, 'home/index.html', context)


def search(request):
    get_method = request.GET.copy()
    key_words = get_method.get('keywords') or None
    product = Product.objects.all()
    product_list = []

    if key_words:
        key_word = get_method.get('keywords')
        product_list = product.filter(product_description__icontains=key_word)

    context = {'categories': Category.objects.all(), 'products': product_list}

    return render(request, 'products/search-result.html', context)
