from django.shortcuts import render
from home.models import Home_Slider, Newsletter, Queries, Banner, Event, Feedback, Deal_of_the_day, shop_by_deals
from accounts.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Category, Subcategory, Product, Main_Category
from django.contrib.auth.decorators import login_required
from cart.models import Wishlist, Cart, CartItem
from datetime import datetime, timedelta
from blog.models import Blog

# emails
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage, BadHeaderError
from django.core import mail
from django.conf import settings
from accounts.views import EmailThread


from django.db.models import Avg
from django.db.models import Count
from django.core.paginator import Paginator

def home(request):
    sliders = Home_Slider.objects.all()
    main_categories = Main_Category.objects.all()

    # this is for top rated categories and products
    # Calculate the average rating for each category
    categories_with_avg_rating = Subcategory.objects.annotate(avg_rating=Avg('products__review_to__rating'))
    
    # Determine the top categories based on the average rating (e.g., top 4 categories)
    top_rated_categories = categories_with_avg_rating.order_by('-avg_rating')[:4]

    # Initialize a list to store top-rated products for each top category
    top_rated_products_by_category = []

    for category in top_rated_categories:
        # Get the top 10 rated products in this category
        top_rated_products = Product.objects.filter(product_category=category) \
            .annotate(avg_rating=Avg('review_to__rating')) \
            .order_by('-avg_rating')[:10]

        top_rated_products_by_category.append({
            'category': category,
            'top_rated_products': top_rated_products,
        })
        
    
    products = Product.objects.all() 
    new_arrivals = products.order_by('product_added_date')[:8]
    special_products = Product.objects.exclude(product_brand="No Brand")[:4]
    banners = Banner.objects.all()
    featured_products = Product.objects.filter(product_featured=True)[:8]
    
    today = datetime.now()
    one_month_ago = today - timedelta(days=7) 
    weekly_products = Product.objects.filter(
        product_added_date__gte=one_month_ago,
        product_added_date__lte=today
    )[:4]
    
    blogs = Blog.objects.all()[:3]
    event = Event.objects.all()[:1]
    feedbacks = Feedback.objects.filter(is_display=True)
    deal_of_the_day = Deal_of_the_day.objects.all()
    flash_products = Product.get_flash_products()[:4]
    shop_by_deal =  shop_by_deals.objects.all()
    context = {
        'sliders': sliders,
        'main_categories': main_categories,
        'top_rated_categories': top_rated_products_by_category,
        'new_arrivals': new_arrivals,
        'special_products': special_products,
        'banners': banners,
        'featured_products': featured_products,
        'weekly_products': weekly_products,
        'blogs': blogs,
        'event': event,
        'feedbacks': feedbacks,
        'deal_of_the_day': deal_of_the_day,
        'flash_products': flash_products,
        'shop_by_deal': shop_by_deal 
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
            messages.success(request, "You have successfully subscribed to Logeachi Newsletter.")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "This e-mail is already subscribed")
            return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        if request.user.is_authenticated:
            email = request.user.email
            gender = request.user.gender
            user_exists = Newsletter.objects.filter(email=email, gender=gender).exists()
            
            if user_exists:
                messages.error(request, 'You have already subscribed our newsletter')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                Newsletter.objects.create(email=email, gender=gender)
                messages.success(request, "You have successfully subscribed to Logeachi Newsletter.")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('signin')

# Search options for keywords
def search(request):
    get_method =  request.GET.copy()
    key_words = get_method.get('keywords') or None
    product = Product.objects.all()
    products = []  
    product_count = 0
    print(key_words)
    if key_words:
        key_word = get_method.get('keywords')
        products = product.filter(product_description__icontains=key_word)
        product_count = products.count()
    

    context= {
        'main_categories': Main_Category.objects.all(),
        'products': products,
        'product_count': product_count,
    }
    

    return render(request, 'products/category_products.html', context)


def about_us(request):
    main_categories = Main_Category.objects.all()
    feedbacks = Feedback.objects.filter(is_display=True)
    context = {
    'main_categories': main_categories,
    'feedbacks': feedbacks
    }
    return render(request, 'home/about_us.html', context=context)


def FAQ(request):
    main_categories = Main_Category.objects.all()
    
    context = {
        'main_categories': main_categories,
    }
    return render(request, 'home/FAQ.html', context=context)


def contact_us(request):
    main_categories = Main_Category.objects.all()
    
    context = {
        'main_categories': main_categories,
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
    

def new_arrivals(request):
    main_categories = Main_Category.objects.all()
    wishlist_count = 0
    today = datetime.now()
    one_month_ago = today - timedelta(days=30) 
    new_arrivals = Product.objects.filter(
        product_added_date__gte=one_month_ago,
        product_added_date__lte=today
    )   
    paginator = Paginator(new_arrivals, 20)
    page_number = request.GET.get('page')
    new_arrivals = paginator.get_page(page_number)
    
    context = {
        'new_arrivals': new_arrivals,
        'main_categories': main_categories,
    }
    
    return render(request, 'products/new_arrivals.html', context)


@login_required
def give_feedback(request):
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        user = request.user
        
        Feedback.objects.create(user=user, feedback=feedback)
        
        messages.success(request, 'Your feedback has been submited')
        return redirect(request.META.get('HTTP_REFERER'))