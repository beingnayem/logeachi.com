from django.shortcuts import render
from  products.models import Product, Category, Main_Category, Subcategory
from django.core.paginator import Paginator
from cart.models import Wishlist

# Create your views here.    

def sub_category_products(request, pk):
    # product_list = Product.objects.filter(category=pk)
    # paginator = Paginator(product_list, 8) # Show 8 products per page
    # page = request.GET.get('page')
    # products = paginator.get_page(page)
    
    
    products = Product.objects.filter(product_category=pk)
    main_categories = Main_Category.objects.all()
    sub_category = None
    category = None
    main_category = None
    
    sub_category = Subcategory.objects.get(id=pk)
    category = sub_category.category
    main_category = category.main_category
    product_count = products.count()
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)

def category_products(request, pk):
    main_categories = Main_Category.objects.all()
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category__category=category)
    product_count = products.count()
    sub_category = None
    main_category = category.main_category
    
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)

def main_category_products(request, pk):
    main_categories = Main_Category.objects.all()
    main_category = Main_Category.objects.get(id=pk)
    products = Product.objects.filter(product_category__category__main_category=main_category)
    product_count = products.count()
    sub_category = None
    category = None
    
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)

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
