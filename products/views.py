from django.shortcuts import render
from  products.models import Product

# Create your views here.


def get_product(request, slug):
    try:
        context = {'products': Product.objects.filter(slug=slug)}
        return render(request, 'products/singel_product.html', context)
    
    except Product.DoesNotExist:
        # handle the case where there is no product with the given slug
        return render(request, 'product_not_found.html')
    


def category_products(request, pk):
    product = Product.objects.filter(category=pk)
    context = {'products': product}
    return render(request, 'products/category-products.html' , context)
