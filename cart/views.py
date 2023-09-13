from django.shortcuts import render, redirect
from products.models import Product
from .models import Wishlist
# Create your views here.

def AddWishlist(request):
    user = request.user
    product_id = request.GET.get('pk')
    product = Product.objects.filter(id=product_id)
    Wishlist(user=user, product=product[0]).save()
    return redirect(request.META.get('HTTP_REFERER'))
    