from django.shortcuts import render, redirect
from customer.models import Address
from .models import Order, OrderItem
from customer.models import Address
from products.models import Product
from cart.models import Cart, CartItem
from .ssl import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal
from django.contrib import messages


# Create your views here.
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    if not cart_item:
        return redirect('home')
    
    addresses = Address.objects.all()
    context = {
        'addresses': addresses
    }
    return render(request, 'order/checkout.html', context)


def place_order(request):
    if request.method == 'POST':
        case_method = request.POST.get('payment')
        if not case_method:
            messages.error(request, 'Please select any payment method')
            return redirect(request.META.get('HTTP_REFERER'))
            
        user = request.user
        billing_address = Address.objects.get(user=user, is_default_shipping=True) 
        shipping_address = Address.objects.get(user=user, is_default_billing=True)
        
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        
        if not billing_address or not shipping_address:
            return redirect(request.META.get('HTTP_REFERER'))
        
        if not cart_item:
            return redirect('home')
        
        order = Order.objects.create(
            user=user,
            billing_address=billing_address,
            shipping_address=shipping_address,
            order_status='processing',
            payment_status='unpaid',
            payment_method='case_on_delivery',
        )

        total = 0
        for item in cart_item:        
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
            total += item.subtotal
            item.delete()
        # added 2% vat
        tax = (2*total)/100
        total = total + tax
        shipping_cost = 1 # shipping 1 $
        
        grand_total = total + shipping_cost
            
        if case_method == 'sslcommerz':
            # convert USD to BDT
            grand_total = (grand_total * 102)
            return redirect(sslcommerz_payment_gateway(request, order.id, grand_total))
        else:
            pass
    return redirect('home')

@method_decorator(csrf_exempt, name='dispatch') # csrf ke disable kore deoya
def success_view(request):
    data = request.POST
    print('================================================================', data)
    order_id = data['value_a']
    user = data['value_b']
    order = Order.objects.get(id=order_id)
    order.payment_method = 'SSLCOMMERZ'
    order.payment_status = 'Paid'
    order.save()
    print('================================================================', order)
    return redirect('home')