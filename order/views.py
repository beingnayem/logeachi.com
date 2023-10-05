from django.shortcuts import render, redirect
from customer.models import Address
from .models import Order, OrderItem, Payment
from customer.models import Address
from products.models import Product
from cart.models import Cart, CartItem
from .ssl import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal
from django.contrib import messages
from accounts.models import User
from django.urls import reverse


# Create your views here.
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)
    total = 0
    for item in cart_item:
        total += item.subtotal
    tax = (5 * total) / 100
    shipping_cost = 80
    grand_total = total + tax + shipping_cost
    if not cart_item:
        return redirect('home')
    
    addresses = Address.objects.all()
    context = {
        'addresses': addresses,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }
    return render(request, 'order/checkout.html', context)


def place_order(request):
    if request.method == 'POST':
        case_method = request.POST.get('payment')
        if not case_method:
            messages.error(request, 'Please select any payment method')
            return redirect(request.META.get('HTTP_REFERER'))
            
        user = request.user
        if Address.objects.filter(user=user, is_default_shipping=True).exists():
            billing_address = Address.objects.get(user=user, is_default_shipping=True)
        else:
            messages.error(request, 'Please select shipping address ')
            return redirect(request.META.get('HTTP_REFERER'))
        if Address.objects.filter(user=user, is_default_billing=True).exists():
            shipping_address = Address.objects.get(user=user, is_default_billing=True)
        else:
            messages.error(request, 'Please select billing address')
            return redirect(request.META.get('HTTP_REFERER'))
        
        if not billing_address or not shipping_address:
            return redirect(request.META.get('HTTP_REFERER'))
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        
        
        if not cart_item:
            return redirect('home')
        
        order = Order.objects.create(
            user=user,
            billing_address=billing_address,
            shipping_address=shipping_address,
            order_status='processing',
        )

        total = 0
        for item in cart_item:        
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
            product = Product.objects.get(id=item.product.pk)
            product.product_quantity -= item.quantity
            product.product_sold_quantity += item.quantity
            product.save()
            
            total += item.subtotal
            item.delete()
        # added 2% vat
        tax = (5 * total) / 100
        shipping_cost = 80
        grand_total = total + tax + shipping_cost
        current_domain = request.META['HTTP_HOST']
        
        if case_method == 'sslcommerz':
            return redirect(sslcommerz_payment_gateway(request, order.id, grand_total, billing_address, current_domain))
        if case_method == 'cash_on_delivery':
            target_url = reverse('success_view_case_on_delivery', args=(order.id, grand_total)) 
            return redirect(target_url)
            
    return redirect('home')

@method_decorator(csrf_exempt, name='dispatch') # csrf ke disable kore deoya
def success_view(request):
    data = request.POST
    
    data = request.POST
    order_id = data['value_a']
    user_id = data['value_b']
    user = User.objects.get(id=user_id)
    address = data['value_c']
    
    billing_address = Address.objects.get(user=user, is_default_shipping=True) 
    shipping_address = Address.objects.get(user=user, is_default_billing=True)
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    
    total = 0
    for item in order_item:
        total += item.subtotal
    tax = (5 * total) / 100
    shipping_cost = 80
    grand_total = total + tax + shipping_cost
    
    payment = Payment.objects.create(
        order = order,
        payment_amount = grand_total,
        payment_method = 'SSLCOMMERZ',
        payment_status = 'Paid'
    ) 
    
    context = {
        'payment': payment,
        'billing_address': billing_address,
        'shipping_address': shipping_address,
        'order': order,
        'order_item': order_item,
        'sub_total': total,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }    

    return render(request, 'order/order_success.html', context)

def success_view_case_on_delivery(request, order_id, grand_total):
    user = request.user
    billing_address = Address.objects.get(user=user, is_default_shipping=True)
    shipping_address = Address.objects.get(user=user, is_default_billing=True) 
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    
    total = 0
    for item in order_item:
        total += item.subtotal
    tax = (5 * total) / 100
    shipping_cost = 80
    grand_total = total + tax + shipping_cost
    
    payment = Payment.objects.create(
        order = order,
        payment_amount = grand_total,
        payment_method = 'CASE ON DELIVERY',
        payment_status = 'Unpaid'
    ) 
    
    context = {
        'payment': payment,
        'billing_address': billing_address,
        'shipping_address': shipping_address,
        'order': order,
        'order_item': order_item,
        'sub_total': total,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
    }
    
    return render(request, 'order/order_case_on_success.html', context)
