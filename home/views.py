from django.shortcuts import render
from home.models import Home_Slider, Newsletter, Queries
from accounts.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Category, Subcategory, Product, Main_Category
from django.contrib.auth.decorators import login_required
from cart.models import Wishlist

# emails
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage, BadHeaderError
from django.core import mail
from django.conf import settings
from accounts.views import EmailThread


def home(request):
    sliders= Home_Slider.objects.all()
    main_categories = Main_Category.objects.all()
    products = Product.objects.all()
    # best_solds = Product.objects.order_by('-product_sold_quantity')[:5]
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
  
                
    context = {
    'sliders': sliders,
    'main_categories': main_categories,
    'products': products,
    # 'best_solds': best_solds,
    'wishlist_count': wishlist_count,
    }
    return render(request, 'home/home.html', context)


def join_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        # Check if a user with the given email exists
        user_exists = Newsletter.objects.filter(email=email).exists()
        
        if not user_exists:
            # If the user does not exist, create a new Subscriber
            Newsletter.objects.create(email=email, gender=gender)
            messages.error(request, "You have successfully subscribed to Logeachi Newsletter.")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "This e-mail is already subscribed")
            return redirect(request.META.get('HTTP_REFERER'))


# Search options for keywords
def search(request):
    get_method =  request.GET.copy()
    key_words = get_method.get('keywords') or None
    product = Product.objects.all()
    products = []  
    print(key_words)
    if key_words:
        key_word = get_method.get('keywords')
        products = product.filter(product_description__icontains=key_word)
    

    context= {
        'categories': Category.objects.all(),
        'products': products
    }
    

    return render(request, 'products/category-products.html', context)


def about_us(request):
    main_categories = Main_Category.objects.all()
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
    'main_categories': main_categories,
    'wishlist_count': wishlist_count,
    }
    return render(request, 'home/about_us.html', context=context)


def FAQ(request):
    main_categories = Main_Category.objects.all()
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
    'main_categories': main_categories,
    'wishlist_count': wishlist_count,
    }
    return render(request, 'home/FAQ.html', context=context)


def contact_us(request):
    main_categories = Main_Category.objects.all()
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
    'main_categories': main_categories,
    'wishlist_count': wishlist_count,
    }
    return render(request, 'home/contact_us.html', context=context)


def send_query(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        query_message = request.POST.get('query_message')
        
        Queries.objects.create(name=name, email=email, subject=subject, query_message=query_message)
        
        # Send Query accepted confirmation email
        current_site = get_current_site(request)
        email_sub = "Query recived confirmation"
        message = render_to_string('adminpanel/query_recived.html', {
            'name': name,
            'subject': subject
        })
        email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
        EmailThread(email_message).start()
        
        messages.error(request, "Your querie has sent. We will reply to you soon.")
        return redirect(request.META.get('HTTP_REFERER'))
    
