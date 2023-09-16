from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from cart.models import Wishlist
from django.contrib.auth.decorators import login_required 
from products.models import Category
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def AddWishlistItem(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user = request.user
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.filter(user=user, product=product).exists()
    if not wishlist:
        Wishlist.objects.create(user=user, product=product)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def ShowWishlist(request):
    if not request.user.is_authenticated:
        return redirect('signin') 
    
    
    categories = Category.objects.all()
    wishlist = Wishlist.objects.filter(user=request.user)
    if not wishlist:
        return render(request, 'wishlist/empty-wishlist.html')
    wishlist_count = 0
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    context = {
        'wishlist': wishlist,
        'wishlist_count': wishlist_count,
        'categories': categories,
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def DeleteWishlistItem(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    wishlist = get_object_or_404(Wishlist, id=id)
    if wishlist:
        wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def clear_wishlist(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user = request.user
    wishlist =Wishlist.objects.get(user=user)
    if wishlist:
        wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER'))

