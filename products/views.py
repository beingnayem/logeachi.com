from django.shortcuts import render
from  products.models import Product, Category
from django.core.paginator import Paginator
from cart.models import Wishlist

# Create your views here.
# def get_product(request, slug):
#     try:
#         context = {'products': Product.objects.filter(slug=slug)}
#         return render(request, 'products/singel_product.html', context)
    
#     except Product.DoesNotExist:
#         # handle the case where there is no product with the given slug
#         return render(request, 'product_not_found.html')
    

def category_products(request, pk):
    # product_list = Product.objects.filter(category=pk)
    # paginator = Paginator(product_list, 8) # Show 8 products per page
    # page = request.GET.get('page')
    # products = paginator.get_page(page)
    products = Product.objects.filter(product_category=pk)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'products/category-products.html', context)


def single_product_page(request, pk):
    product = Product.objects.get(id=pk)
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        'product': product,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/single_product_page.html', context)
