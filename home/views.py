from django.shortcuts import render
# from products.models import Product, Category
from home.models import Banner
from django.core.paginator import Paginator
from django.shortcuts import render


def home(request):
    sliders= Banner.objects.filter(banner_type='slider')
    newslatters= Banner.objects.filter(banner_type='newslatter')
    # print('===================================================================================')
    # print(newslatters[0].banner_name)
    context = {
    'sliders': sliders,
    'newslatters': newslatters
    }
    return render(request, 'home/home.html', context)


# Search options for keywords
# def search(request):
#     get_method =  request.GET.copy()
#     key_words = get_method.get('keywords') or None
#     product = Product.objects.all()
#     product_list = []  # Initialize product_list to an empty list

#     if key_words:
#         key_word = get_method.get('keywords')
#         product_list = product.filter(product_description__icontains=key_word)

#     context= {'categories': Category.objects.all(),'products': product_list}

#     return render(request, 'products/search-result.html', context)

