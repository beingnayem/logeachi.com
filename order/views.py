from django.shortcuts import render, redirect
from customer.models import Address
from .models import Order, OrderItem
from customer.models import Address
from products.models import Product
from cart.models import Cart, CartItem

# Create your views here.
def checkout(request):
    addresses = Address.objects.all()
    context = {
        'addresses': addresses
    }
    return render(request, 'order/checkout.html', context)

def place_order(request):
    if request.method == 'POST':
        case_method = request.POST.get('payment')
        user = request.user
        billing_address = Address.objects.get(is_default_shipping=True) 
        shipping_address = Address.objects.get(is_default_billing=True)
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        
        if not billing_address or not shipping_address:
            return redirect(request.META.get('HTTP_REFERER'))
        
        if case_method == 'cash_on_delivery' and cart_item:
            order = Order.objects.create(
                user=user,
                billing_address=billing_address,
                shipping_address=shipping_address,
                order_status='processing',
                payment_status='unpaid',
                payment_method='case_on_delivery',
            )

            for item in cart_item:        
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
                item.delete()
                
            cart.delete()
            
        elif case_method == 'sslcommerz':
            pass
        else:
            pass
        
    return redirect('home')