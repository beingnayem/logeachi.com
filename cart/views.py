from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Wishlist
from django.contrib.auth.decorators import login_required 
from products.models import Category
# Create your views here.

@login_required
def AddWishlist(request):
    user = request.user
    product_id = request.GET.get('pk')
    product = Product.objects.filter(id=product_id)
    wishlist = Wishlist.objects.filter(user=user, product=product[0])
    if not wishlist:
        Wishlist(user=user, product=product[0]).save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def ShowWishlist(request):
    categories = Category.objects.all()
    wishlists = Wishlist.objects.filter(user=request.user)
    if not wishlists:
        return render(request, 'wishlist/empty_wishlist.html')
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    context = {
        'wishlists': wishlists,
        'wishlist_count': wishlist_count,
        'categories': categories,
    }
    return render(request, 'wishlist/show_wishlist.html', context)

@login_required
def DeleteWishlist(request):
    product_id = request.GET.get('pk')
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user, product=product)
    if wishlist:
        wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER'))