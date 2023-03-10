from django.shortcuts import render
from accounts.models import User, Address
from products.models import * 
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def removecart(request):
    if request.method == 'GET':
        pk = request.GET['pk']
        c= Cart.objects.get(Q(product=pk) & Q(user=request.user))
        c.delete()        
        return redirect(request.META.get('HTTP_REFERER'))
        

@login_required
def addTOwishlist(request):
    user = request.user
    product_id = request.GET.get('pk')
    product = Product.objects.get(pk=product_id)
    wishlist = Wishlist.objects.filter(user=user, product=product)
    if not wishlist.exists():
        Wishlist(user=user, product=product).save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def ShowWishlist(request):
    if not request.user.is_authenticated:
        return redirect('signin') 
    
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    if not wishlist:
        return render(request, 'wishlist/empty_wishlist.html')
    else:
        return render(request, 'wishlist/wishlist.html', locals())


@login_required
def RemoveWishlist(request):
    user = request.user
    product_id = request.GET.get('pk')
    product = get_object_or_404(Product, pk=product_id)
    wishlist = get_object_or_404(Wishlist, user=user, product=product)
    
    if wishlist:
        wishlist.delete()
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    shipping_addresses = Address.objects.filter(customer=request.user)
    shipping_cost = 50
    context = {
        'cart_items': cart_items,
        'shipping_addresses': shipping_addresses,
        'shipping_cost' : shipping_cost
    }

    total_cost = sum(item.total_cost for item in cart_items)
    context['total_cost'] = total_cost+shipping_cost

    if request.method == 'POST':
        address_id = request.POST.get('shipping_address')
        if address_id:
            selected_address = Address.objects.get(pk=address_id)
            context['selected_address'] = selected_address

    return render(request, 'cart/checkout.html', context)





from django.contrib import messages
from django.utils import timezone

def place_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('shipping_address_id')
        if not address_id:
            messages.error(request, 'Please select a shipping address.')
            return redirect('checkout')
        selected_address = Address.objects.get(pk=address_id)

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('checkout')

        # Create the order
        shipping_cost = 50
        order = Order.objects.create(
            customer=request.user,
            shipping_address=selected_address,
            shipping_cost=shipping_cost,
            order_date=timezone.now(),
        )

        # Add each cart item to the order
        total_cost = 0
        for cart_item in cart_items:
            order_line_item = OrderLineItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
            total_cost += order_line_item.quantity * order_line_item.product.price

        # Update the order's total cost
        order.total_cost = total_cost + shipping_cost
        order.save()

        # Clear the user's cart
        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully.')
        return redirect('home')





