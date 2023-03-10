from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator


# Create your views here.


def get_product(request, slug):
    try:
        context = {'products': Product.objects.filter(slug=slug)}
        return render(request, 'products/singel_product.html', context)

    except Product.DoesNotExist:

        return render(request, 'product_not_found.html')


def category_products(request, pk, page):
    product_list = Product.objects.filter(category=pk)
    paginator = Paginator(product_list, 8)  # Show 8 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products}
    return render(request, 'products/category-products.html', context)
