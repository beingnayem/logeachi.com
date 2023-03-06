from django.shortcuts import render
from accounts.models import User
from products.models import Category, Cart, Product, Wishlist
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.


def addTOcart(request):
    if not request.user.is_authenticated:
        return redirect('signin') 

    product_id = request.GET.get('pk')
    product = Product.objects.get(pk=product_id)

    # Check if the product is already in the user's cart
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart(user=request.user, product=product, quantity=1).save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Showcart(request):
    if not request.user.is_authenticated:
        return redirect('signin') 
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    total_ammount=0
    shipping_cost = 50
    if not cart:
        return render(request, 'cart/empty_cart.html')
    else:
        for p in cart:
            total_ammount += (p.quantity*p.product.price)
        total_cost = total_ammount+shipping_cost
        return render(request, 'cart/cart.html', locals())


def pluscart(request):
    if request.method == 'GET':
        pk = request.GET['pk']
        c = Cart.objects.get(Q(product=pk) & Q(user=request.user))
        
        if c.quantity >= c.product.quantity:
            # Return a message indicating that the product quantity cannot be increased further
            data = {
                'message': 'The product quantity cannot be increased further.'
            }
        else:
            c.quantity += 1
            c.save()
            
            user = request.user
            cart = Cart.objects.filter(user=user)
            total_ammount = 0
            shipping_cost = 50
            
            for p in cart:
                total_ammount += (p.quantity * p.product.price)
                
            total_cost = total_ammount + shipping_cost
            
            data = {
                'quantity': c.quantity,
                'total_ammount': total_ammount,
                'total_cost': total_cost
            }

        return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        pk = request.GET['pk']
        cart_obj = Cart.objects.get(Q(product=pk) & Q(user=request.user))
        cart_obj.quantity -= 1

        if cart_obj.quantity == 0:
            cart_obj.delete()
        else:
            cart_obj.save()

        user = request.user
        cart = Cart.objects.filter(user=user)
        total_ammount = 0
        shipping_cost = 50
        for p in cart:
            total_ammount += (p.quantity*p.product.price)
        total_cost = total_ammount + shipping_cost

        data = {
            'quantity': cart_obj.quantity,
            'total_ammount': total_ammount,
            'total_cost': total_cost
        }

        return JsonResponse(data)
    

def removecart(request):
    if request.method == 'GET':
        pk = request.GET['pk']
        c= Cart.objects.get(Q(product=pk) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        
        total_ammount=0
        shipping_cost = 50
        for p in cart:
            total_ammount += (p.quantity*p.product.price)
        
        total_cost = total_ammount+shipping_cost

        data = {
            'total_ammount': total_ammount,
            'total_cost': total_cost
        }

        return JsonResponse(data)
        

def addTOwishlist(request):
    user = request.user
    product_id = request.GET.get('pk')
    product = Product.objects.get(pk=product_id)
    wishlist = Wishlist.objects.filter(user=user, product=product)
    if not wishlist.exists():
        Wishlist(user=user, product=product).save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def ShowWishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist/wishlist.html', locals())


