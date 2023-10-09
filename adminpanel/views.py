from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.views.generic import View
from products.models import Product, Main_Category, Category, Subcategory
from django.contrib import messages
from django.contrib.auth.tokens  import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.utils import TokenGenerator, generate_token
from home.models import Queries, Home_Slider, Banner, Event, Feedback, Deal_of_the_day, shop_by_deals
from blog.models import Blog
from utils.image_resizer import resize_image
from order.models import Order, OrderItem, Payment
from django.db.models import Sum

# emails
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage, BadHeaderError
from django.core import mail
from django.conf import settings
from accounts.views import EmailThread

# Create your views here.



@login_required
def adminPanelView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    orders = Order.objects.all()[0:7]
    
    # Total number of orders
    total_orders = Order.objects.all().count()

    # Total sales amount
    total_sale = Payment.objects.aggregate(Sum('payment_amount'))['payment_amount__sum']

    # Handle the case where total_sale might be None
    total_sale = total_sale if total_sale is not None else 0
    
    total_profit = Payment.objects.aggregate(Sum('raw_profit'))['raw_profit__sum']
    top_sold_products = Product.objects.order_by('-product_sold_quantity')[:10]
    
    context = {'total_orders': total_orders, 'total_sale': total_sale, 'orders': orders , 'total_profit': total_profit, 'top_sold_products': top_sold_products}
    
    return render(request, 'adminpanel/admin_dashboard.html', context)

@login_required
def team_memberView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    team_members= User.objects.filter(is_admin=True)
    return render(request, 'adminpanel/team_member.html', {'team_members': team_members})


@login_required
def admin_request_listView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    admin_requests = User.objects.filter(admin_request='requested')
    return render(request, 'adminpanel/admin_request_list.html', {'admin_requests': admin_requests})
 
@login_required
def admin_request_approve(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        approve_by = request.user
        try:
            user = User.objects.get(id=id, admin_request='requested')
            user.is_active = True
            user.is_admin= True
            user.admin_request='approved'
            user.save()
        # Send approve email
            current_domain = request.META['HTTP_HOST']
            email_sub = "Welcome Aboard! 🌟 Your Admin Request has been Approved!"
            message = render_to_string('adminpanel/admin_request_approve_email.html', {
                'user': user,
                'approve_by': approve_by,
                'current_domain': current_domain
            })
            email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
            
            messages.success(request, 'Admin request approve succesfull')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('admin_request_list')


@login_required
def admin_request_decline(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        try:
            user = User.objects.get(id=id, admin_request='requested')
            # print('=========================================================', user)
            user.is_active = True
            user.is_admin= False
            user.admin_request=None
            user.save()
            
            # Send decline email
            current_domain = request.META['HTTP_HOST']
            email_sub = "Your Application for Admin Position at Logeachi Dot Com"
            message = render_to_string('adminpanel/admin_request_decline_email.html', {
                'user': user,
                'current_domain': current_domain
            })
            email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
        
            messages.success(request, 'Admin request decline succesfull')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('admin_request_list')


@login_required
def remove_admin(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(id=id, is_admin=True)
            if not user.email==request.user.email:
                user.is_active = True
                user.is_admin= False
                user.admin_request=None
                user.save()
                
                # Send termination email
                current_domain = request.META['HTTP_HOST']
                email_sub = "Termination of Employment"
                today = timezone.now()
                effective_date = today + timedelta(days=7)
                message = render_to_string('adminpanel/remove_admin_email.html', {
                    'user': user,
                    'effective_date': effective_date,
                    'currrnt_domain': current_domain
                })
                email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
                EmailThread(email_message).start()
                
                messages.success(request, 'Admin removed succesfull')
                return redirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, 'Current admin can not remove himself')
                return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('team_member')


@login_required
def remove_user(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        try:
            user = User.objects.get(id=id)
            if not user.email==request.user.email:
                user.delete()
                
                # Send Account Deletion Confirmation email
                current_domain = request.META['HTTP_HOST']
                user_first_name = user.first_name
                email_sub = 'Account Deletion Confirmation'
                message = render_to_string('adminpanel/remove_user_email.html', {
                    'user_first_name': user_first_name,
                    'current_domain': current_domain
                })
                email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
                EmailThread(email_message).start()
                
                messages.success(request, 'User Remove succesfull')
                return redirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, 'Current admin can not remove himself')
                return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('team_member')


@login_required
def customerView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    customers= User.objects.filter(is_admin=False)
    return render(request, 'adminpanel/customer_list.html', {'customers': customers})


@login_required
def productView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    products= Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})


@login_required
def add_product(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting product data
    if request.method == 'POST':
        try:
            # Retrieve product data from the request
            product_name = request.POST.get('product_name')
            product_image = request.FILES.get('product_image')
            product_brand = request.POST.get('product_brand')
            product_category_id = request.POST.get('product_category')
            product_price = request.POST.get('product_price')
            product_description = request.POST.get('product_description')
            product_quantity = request.POST.get('product_quantity')
            product_location = request.POST.get('product_location')
            product_warrenty = request.POST.get('product_warrenty')
            product_cash_payment = request.POST.get('product_cash_payment')
            product_online_payment = request.POST.get('product_online_payment')
            product_return = request.POST.get('product_return')
            product_featured = request.POST.get('product_featured')
            product_flash_expiry_str = request.POST.get('product_flash_expiry')
        
            # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
            product_flash_expiry = datetime.strptime(product_flash_expiry_str, '%Y-%m-%d')
            
            # resize the product_image to match our requirements
            if product_image:
                resized_product_image = resize_image(product_image, 600, 600)
            
            # Get the Subcategory instance by name
            product_category = Subcategory.objects.get(id=product_category_id)
            
            # Create product
            Product.objects.create(
                product_name=product_name,
                product_image=resized_product_image,
                product_brand=product_brand,
                product_category=product_category,
                product_price=product_price,
                product_description=product_description,
                product_quantity=product_quantity,
                product_location=product_location,
                product_warrenty=product_warrenty,
                product_cash_payment=product_cash_payment,
                product_online_payment=product_online_payment,
                product_return=product_return,
                product_featured=product_featured,
                product_flash_expiry = product_flash_expiry
            )
            
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
        
        except Exception as e:
            messages.error(request, f"Error creating product: {e}")
            return redirect('add_product')

    # If it's a GET request, fetch an empty list of categories
    else:
        sub_categories = Subcategory.objects.all()
        return render(request, 'adminpanel/add_product.html', {'sub_categories': sub_categories})


@login_required
def edit_product(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the product list without showing the success message
        return redirect('product_list')
    
    if request.method == 'POST':
        try:
            # get product by id
            product_id = request.POST.get('id')
            product = Product.objects.get(id=product_id)

            # Retrieve product data from the request
            product_name = request.POST.get('product_name')
            product_image = request.FILES.get('product_image')
            product_brand = request.POST.get('product_brand')
            product_category_id = request.POST.get('product_category')
            product_price = request.POST.get('product_price')
            product_description = request.POST.get('product_description')
            product_quantity = request.POST.get('product_quantity')
            product_location = request.POST.get('product_location')
            product_warrenty = request.POST.get('product_warrenty')
            product_cash_payment = request.POST.get('product_cash_payment')
            product_online_payment = request.POST.get('product_online_payment')
            product_return = request.POST.get('product_return')
            product_featured = request.POST.get('product_featured')
            product_flash_expiry_str = request.POST.get('product_flash_expiry')
            
            # Update product details and save the object in the database
            product.product_name = product_name
            if product_image:
                resized_product_image = resize_image(product_image, 600, 600)
                product.product_image = resized_product_image
            product.product_brand = product_brand
            if product_category_id:
                product_category = get_object_or_404(Subcategory, id=product_category_id)
                product.product_category = product_category
            product.product_price = product_price
            product.product_description = product_description
            product.product_quantity = product_quantity
            product.product_location = product_location
            if product_warrenty:
                product.product_warrenty = product_warrenty
            if product_cash_payment:
                product.product_cash_payment = product_cash_payment
            if product_online_payment:
                product.product_online_payment = product_online_payment
            if product_return:
                product.product_return = product_return
            if product_featured:
                product.product_featured = product_featured
            if product_flash_expiry_str:
                # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
                product_flash_expiry = datetime.strptime(product_flash_expiry_str, '%Y-%m-%d')
                product.product_flash_expiry = product_flash_expiry
            product.save()
            
            messages.success(request, 'Product edited successfully.')
            return redirect('product_list')
        
        except Exception as e:
            messages.error(request, f"Error editing product: {e}")
            return redirect('product_list')
    
    # If it's a GET request, fetch the list of categories and render the edit form
    product_id = request.GET.get('id')
    product =Product.objects.get(id=product_id)
    categories = Subcategory.objects.all()
    
    return render(request, 'adminpanel/edit_product.html', {'categories': categories, 'product': product})


@login_required
def delete_product(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        try:
            # get product by id
            pk = request.POST.get('pk')
            product = get_object_or_404(Product, pk=pk)
            product.delete()

            messages.success(request, 'Product deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error editing product: {e}")
            messages.error(request, 'An error occurred while deleting the product.')
            return redirect('product_list')
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def restock_product(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the product list without showing the success message
        return redirect('product_list')
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('id')
            stock_quantity = request.POST.get('stock_quantity')
            
            product= Product.objects.get(id=product_id)
            
            stock_quantity = product.product_quantity+ int(stock_quantity)
            product.product_quantity = stock_quantity
            product.product_stock_date = timezone.now()
            product.save()
            
            messages.success(request, "Product restock successfull")
            return redirect('product_list')
        
        except Exception as e:
            print(f"Error restock product: {e}")
            messages.error(request, 'An error occurred while restock the product.')
            return redirect('product_list')
    
    # If it's a GET request, fetch the product and render the restock form
    product_id = request.GET.get('id')
    product =Product.objects.get(id=product_id)
    
    return render(request, 'adminpanel/restock_product.html', {'product': product})


@login_required
def individual_product_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        
        return render(request, 'adminpanel/individual_product_details.html', {'product': product})
    

class admin_signup_requestView(View):

    def get(self, request):
        if not request.user.is_admin:
            return render(request, 'accounts/wrong_path.html')
        return render(request, 'adminpanel/admin_signup_request.html')

    def post(self, request):
        if not request.user.is_admin:
            return render(request, 'accounts/wrong_path.html')
        
        email = request.POST['email']
        first_name="admin"
        last_name="here"
        gender= "male"
        password = "admin"
        userExist = User.objects.filter(email=email).exists()

        if not userExist:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, password=password)
            user.is_active = False
            user.save()
            
            current_domain = request.META['HTTP_HOST']
            email_sub = "Admin signup request"
            message = render_to_string('adminpanel/admin_signup_email.html', {
                    'current_domain': current_domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': PasswordResetTokenGenerator().make_token(user)
                })

            email_message = EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
            messages.info(request, "Admin signup link e-mail sent successfully")
            return render(request, 'adminpanel/admin_signup_request.html')

        else:
            messages.error(request, "This email is already registered")
            return render(request, 'adminpanel/admin_signup_request.html')


class admin_signupView(View):

    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token' : token
        }
         
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            # print(f"user_id type: {type(user_id)}, value: {user_id}")
            user = User.objects.get(pk=user_id)
            # print(f"user type: {type(user)}, value: {user}")
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password reset e-mail link is invalid")
                return render(request, 'accounts/not_valid_link.html')
 
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            messages.error(request, "Invalid user")
            return render(request, 'adminpanel/admin_signup_request.html')
            
        return render(request, 'adminpanel/admin_signup.html', context)

    def post(self, request, uidb64, token):
        
        context = {
            'uidb64': uidb64,
            'token' : token
        }
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        
        if password != confirm_password:
            messages.error(request, "Password is not matching")
            return render(request, 'accounts/admin_signup.html', context)
        
        user = User.objects.get(email=email)
        
        if user:
            if user.is_active==False and user.admin_request==None:
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.admin_request='requested'
                user.is_active = False
                user.set_password(password)
                user.save()
                messages.success(request, "Account has been created and pending for approve by admin.")
                return redirect('home')
            else:
                messages.error(request, "You are not slected for admin")
                return redirect('home')
        else:
            messages.error(request, "This email doesn't exist in our employee recomendations")
            return redirect('home')
        
        return render(request, 'adminpanel/admin_signup.html', context)   
    
    
@login_required
def queries(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    queries = Queries.objects.all()
    return render(request, 'adminpanel/queries.html', {'queries': queries})


@login_required
def view_query(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    query_id = request.GET.get('id')
    query = Queries.objects.get(id=query_id)
    formatted_query_date = query.query_date.strftime('%Y-%m-%d')
    formatted_reply_date = query.reply_date.strftime('%Y-%m-%d')
    context = {
        'query': query, 
        'formatted_query_date': formatted_query_date, 
        'formatted_reply_date': formatted_reply_date
    }
    return render(request, 'adminpanel/view_query.html', context)


@login_required
def reply_query(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        query_id = request.POST.get('id')
        query_reply = request.POST.get('query_reply')
        
        query = Queries.objects.get(id=query_id)
        email = query.email
        name = query.name
        subject = query.subject

        try:
            # Send Query Reply email
            current_site = get_current_site(request)
            email_sub = "Query Reply"
            message = render_to_string('adminpanel/query_replyed_email.html', {
                'name': name,
                'subject': subject,
                'query_reply': query_reply
            })
            email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()

        except Exception as e:
            print(f"Error Sending Email: {e}")
            messages.error(request, 'An error occurred while sending email.')
            return redirect('queries')
        
        query.query_status = 'replyed'
        query.query_reply = query_reply
        query.reply_date = timezone.now()
        query.save()
        
        messages.success(request, 'Query reply succesfull')
        return redirect('queries')

    # If the request method is GET
    query_id = request.GET.get('id')
    query = Queries.objects.get(id=query_id)
    formatted_query_date = query.query_date.strftime('%Y-%m-%d')
    context = {
        'query': query, 
        'formatted_query_date': formatted_query_date, 
    }
    
    return render(request, 'adminpanel/query_reply.html', context)


@login_required
def main_categoryView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    main_categories= Main_Category.objects.all()
    return render(request, 'adminpanel/main_category_list.html', {'main_categories': main_categories})


@login_required
def categoryView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    categories= Category.objects.all()
    return render(request, 'adminpanel/category_list.html', {'categories': categories})


@login_required
def sub_categoryView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    sub_categories= Subcategory.objects.all()
    return render(request, 'adminpanel/sub_category_list.html', {'sub_categories': sub_categories})


@login_required
def add_main_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting main category data
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            
            Main_Category.objects.create(name=name)

            messages.success(request, 'Main Category added successfully')
            return redirect('main_category_list')
        
        except Exception as e:
            messages.error(request, 'An error occurred while adding mian category.')
            return redirect('main_category_list')
        
    # If it's a GET request
    else:
        return render(request, 'adminpanel/add_main_category.html')


@login_required
def add_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting category data
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            main_category_id = request.POST.get('main_category_id')
            
            main_category = Main_Category.objects.get(id=main_category_id)

            Category.objects.create(name=name, main_category=main_category)

            messages.success(request, 'Category added successfully')
            return redirect('category_list')
        
        except Exception as e:
            messages.error(request, 'An error occurred while adding category.')
            return redirect('category_list')
        
    # If it's a GET request, fetch an empty list of main categories
    else:
        main_categories = Main_Category.objects.all()
        return render(request, 'adminpanel/add_category.html', {'main_categories': main_categories})
  

@login_required
def add_sub_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting sub category data
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            
            category = Category.objects.get(id=category_id)
            
            Subcategory.objects.create(name=name, category=category)

            messages.success(request, 'Sub Category added successfully')
            return redirect('sub_category_list')
        
        except Exception as e:
            print(f"Error adding sub category: {e}")
            messages.error(request, 'An error occurred while adding sub category.')
            return redirect('sub_category_list')
            
        
    # If it's a GET request, fetch an empty list of categories
    else:
        categories = Category.objects.all()
        return render(request, 'adminpanel/add_sub_category.html', {'categories': categories})
    
    
@login_required
def edit_main_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the main category list without showing the success message
        return redirect('main_category_list')
    
    if request.method == 'POST':
        try:
            # get main_category by id
            main_category_id = request.POST.get('main_category_id')
            main_category = Main_Category.objects.get(id=main_category_id)
            
            # Retrieve main category data from the request
            name = request.POST.get('name')
            
            if main_category:
                if name:
                    main_category.name = name 
                main_category.save()
                
                messages.success(request, 'Main Category Edited Successfully.')
                return redirect('main_category_list')
        
        except Exception as e:
            messages.error(request, 'An error occurred while editing the main category.')
            return redirect('main_category_list')
    
    # If it's a GET request
    main_category_id = request.GET.get('main_category_id')
    main_category = Main_Category.objects.get(id=main_category_id)
    
    return render(request, 'adminpanel/edit_main_category.html', {'main_category': main_category})


@login_required
def edit_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the category list without showing the success message
        return redirect('category_list')
    
    if request.method == 'POST':
        try:
            # get category by id
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            main_category_id = request.POST.get('main_category_id')
            category = Category.objects.get(id=category_id)
            
            
            # Retrieve category data from the request
            
            if category:
                if name:
                    category.name = name 
                if main_category_id:
                    main_category = Main_Category.objects.get(id=main_category_id)
                    category.main_category=main_category
                category.save()
                
                messages.success(request, 'Category edited successfully.')
                return redirect('category_list')
        
        except Exception as e:
            messages.error(request, 'An error occurred while editing the category.')
            return redirect('category_list')
    
    # If it's a GET request, fetch the list of main categories and render the edit form
    category_id = request.GET.get('category_id')
    category = Category.objects.get(id=category_id)
    main_categories = Main_Category.objects.all()
    
    return render(request, 'adminpanel/edit_category.html', {'category': category, 'main_categories': main_categories})


@login_required
def edit_sub_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the category list without showing the success message
        return redirect('sub_category_list')
    
    if request.method == 'POST':
        try:
            # get sub category by id
            name = request.POST.get('name')
            sub_category_id = request.POST.get('sub_category_id')
            category_id = request.POST.get('category_id')
            sub_category = Subcategory.objects.get(id=sub_category_id)
            
            # Retrieve sub category data from the request
            
            if sub_category:
                if name:
                    sub_category.name = name 
                if category_id:
                    category = Category.objects.get(id=category_id)
                    sub_category.category = category
                sub_category.save()
                
                messages.success(request, 'Sub Category edited successfully.')
                return redirect('sub_category_list')
        
        except Exception as e:
            messages.error(request, 'An error occurred while editing the sub category.')
            return redirect('sub_category_list')
    
    # If it's a GET request, fetch the list of categories and render the edit form
    sub_category_id = request.GET.get('sub_category_id')
    sub_category = Subcategory.objects.get(id=sub_category_id)
    categories = Category.objects.all()
    
    return render(request, 'adminpanel/edit_sub_category.html', {'sub_category': sub_category, 'categories': categories})
    
    
@login_required
def delete_main_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get main category by id
            main_category_id = request.GET.get('main_category_id')
            main_category = get_object_or_404(Main_Category, id=main_category_id)
            main_category.delete()

            messages.success(request, 'Main Category deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting main category: {e}")
            messages.error(request, 'An error occurred while deleting the main category.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get category by id
            category_id = request.GET.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category.delete()

            messages.success(request, 'Category deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting category: {e}")
            messages.error(request, 'An error occurred while deleting the category.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def delete_sub_category(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get sub category by id
            sub_category_id = request.GET.get('sub_category_id')
            sub_category = get_object_or_404(Subcategory, id=sub_category_id)
            sub_category.delete()

            messages.success(request, 'Sub Category deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting sub category: {e}")
            messages.error(request, 'An error occurred while deleting the sub category.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def add_slider(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting sub category data
    if request.method == 'POST':
        try:
            slider_banner =  request.FILES.get('slider_banner')
            slider_title = request.POST.get('slider_title')
            offer = request.POST.get('offer')
            offer_description = request.POST.get('offer_description')
            starting_price = request.POST.get('starting_price')
            category_id = request.POST.get('category_id')
            
            category = Category.objects.get(id=category_id)
            
            slider = Home_Slider.objects.create(slider_banner=slider_banner, slider_product_category=category)    
            
            if slider_title:
                slider.slider_offer_title = slider_title
            if offer:
                slider.slider_offer = offer
            if offer_description:
                slider.slider_offer_description = offer_description
            if starting_price:
                slider.slider_offer_starting_price = starting_price
            slider.save()

            messages.success(request, 'Slider added successfully')
            return redirect('sliders')

        except Exception as e:
            # print(f"Error adding slider: {e}")
            messages.error(request, f'{e}')
            return redirect('sliders')
            
    categories = Category.objects.all()
    return render(request, 'adminpanel/add_slider.html', {'categories': categories})


@login_required
def delete_slider(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get sub category by id
            slider_id = request.GET.get('slider_id')
            slider = get_object_or_404(Home_Slider, id=slider_id)
            slider.delete()

            messages.success(request, 'Slider deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting slider: {e}")
            messages.error(request, 'An error occurred while deleting the slider.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def edit_slider(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the category list without showing the success message
        return redirect('sliders')
    
    if request.method == 'POST':
        try:
            # Retrieve data from the request
            slider_id = request.POST.get('slider_id')
            slider_banner = request.FILES.get('slider_banner')
            slider_title = request.POST.get('slider_title')
            offer = request.POST.get('offer')
            offer_description = request.POST.get('offer_description')
            starting_price = request.POST.get('starting_price')
            category_id = request.POST.get('category_id')

            # Fetch the slider object
            slider = Home_Slider.objects.get(id=slider_id)

            if slider:
                # Update slider attributes, including 'slider_banner' if a new file is provided
                if slider_banner:
                    slider.slider_banner = slider_banner
                if category_id:
                    category = Category.objects.get(id=category_id)
                    slider.slider_product_category = category
                if slider_title:
                    slider.slider_offer_title = slider_title
                if offer:
                    slider.slider_offer = offer
                if offer_description:
                    slider.slider_offer_description = offer_description
                if starting_price:
                    slider.slider_offer_starting_price = starting_price
                slider.save()

                messages.success(request, 'Slider edited successfully.')
                return redirect('sliders')

        except Exception as e:
            # print(f"Error editing slider: {e}")
            messages.error(request, f"Error editing slider: {e}")
            return redirect('sliders')

    
    # If it's a GET request, fetch the list of slider and render the edit form
    slider_id = request.GET.get('slider_id')
    slider = Home_Slider.objects.get(id=slider_id)
    categories = Category.objects.all()
    return render(request, 'adminpanel/edit_slider.html', {'slider': slider, 'categories': categories})


@login_required
def slider_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        slider_id = request.POST.get('slider_id')
        slider = Home_Slider.objects.get(id=slider_id)
        
        return render(request, 'adminpanel/slider_details.html', {'slider': slider})


@login_required
def slidersView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    sliders = Home_Slider.objects.all()
    return render(request, 'adminpanel/sliders.html', {'sliders': sliders})


@login_required
def add_banner(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting banner data
    if request.method == 'POST':
        try:
            banner_image = request.FILES.get('banner_image')
            banner_title = request.POST.get('banner_title')
            banner_offer = request.POST.get('banner_offer')
            category_id = request.POST.get('category_id')
            
            # get the category object from the category model
            banner_product_category = Category.objects.get(id=category_id)

            banner = Banner.objects.create(banner_image=banner_image, banner_product_category=banner_product_category)   
            
            if banner_title:
                banner.banner_title=banner_title
            if banner_offer:
                banner.banner_offer=banner_offer
            banner.save

            messages.success(request, 'Banner added successfully')
            return redirect('banners')

        except Exception as e:
            # print(f"Error adding slider: {e}")
            messages.error(request, f"Error adding slider: {e}")
            return redirect('banners')
        
    else:
        categories = Category.objects.all()
        return render(request, 'adminpanel/add_banner.html', {'categories': categories})


@login_required
def delete_banner(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get banner by id
            banner_id = request.GET.get('banner_id')
            banner = get_object_or_404(Banner, id=banner_id)
            banner.delete()

            messages.success(request, 'Banner deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting banner: {e}")
            messages.error(request, 'An error occurred while deleting the banner.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def edit_banner(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the category list without showing the success message
        return redirect('banners')
    
    if request.method == 'POST':
        try:
            # Retrieve data from the request
            banner_id = request.POST.get('banner_id')
            banner_image = request.FILES.get('banner_image')
            banner_title = request.POST.get('banner_title')
            banner_offer = request.POST.get('banner_offer')
            category_id = request.POST.get('category_id')
            
            # get the banner object
            banner = Banner.objects.get(id=banner_id)

            if banner:
                # Update slider attributes, including 'banner image' if a new file is provided
                if banner_image:
                    banner.banner_image = banner_image
                if banner_title:
                    banner.banner_title=banner_title
                if banner_offer:
                    banner.banner_offer=banner_offer
                if category_id:
                    banner_product_category = Category.objects.get(id=category_id)
                    banner.banner_product_category = banner_product_category
                banner.save()

                messages.success(request, 'Banner edited successfully.')
                return redirect('banners')

        except Exception as e:
            print(f"Error editing slider: {e}")
            messages.error(request, f"Error editing slider: {e}")
            return redirect('banners')

    # If it's a GET request, fetch the list of baner, categories and render the edit form
    banner_id = request.GET.get('banner_id')
    banner = Banner.objects.get(id=banner_id)
    categories = Category.objects.all()
    
    return render(request, 'adminpanel/edit_banner.html', {'banner': banner, 'categories': categories})


@login_required
def banner_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        banner_id = request.POST.get('banner_id')
        banner = Banner.objects.get(id=banner_id)
        
        return render(request, 'adminpanel/banner_details.html', {'banner': banner})


@login_required
def bannersView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    banners = Banner.objects.all()
    
    return render(request, 'adminpanel/banners.html', {'banners': banners})

    
@login_required   
def blogsView(request):
    
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    blogs= Blog.objects.all()
    return render(request, 'adminpanel/blogs.html', {'blogs': blogs})


@login_required
def post_blog(request):
    
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'POST':
        try:
            blog_image = request.FILES.get('blog_image')
            blog_title = request.POST.get('blog_title')
            blog_topic = request.POST.get('blog_topic')
            blog_writer = request.POST.get('blog_writer')
            blog_text = request.POST.get('blog_text')
            
            Blog.objects.create(blog_image=blog_image, blog_title=blog_title, blog_topic=blog_topic, blog_writer=blog_writer, blog_text=blog_text)

            messages.success(request, 'Blog posted successfully')  # Use messages.success for success messages
            return redirect('blogs')
        
        except Exception as e:
            print(f"Error posting blog: {e}")
            messages.error(request, 'An error occurred while posting blog.')
            return redirect(request.META.get('HTTP_REFERER'))
            
    
    return render(request, 'adminpanel/post_blog.html')


@login_required
def edit_blog(request):
    
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the blog list without showing the success message
        return redirect('blogs')
    
    if request.method == 'POST':
        try:
            blog_id = request.POST.get('blog_id')
            blog_image = request.FILES.get('blog_image')
            blog_title = request.POST.get('blog_title')
            blog_topic = request.POST.get('blog_topic')
            blog_writer = request.POST.get('blog_writer')
            blog_text = request.POST.get('blog_text')
            
            blog = Blog.objects.get(id=blog_id)

            if blog_image:
                blog.blog_image = blog_image
            blog.blog_title = blog_title
            blog.blog_topic = blog_topic
            blog.blog_writer = blog_writer
            blog.blog_text = blog_text
            blog.save()
            
            messages.success(request, 'Blog edited successfully')  # Use messages.success for success messages
            return redirect('blogs')
        
        except Exception as e:
            print(f"Error editing blog: {e}")
            messages.error(request, 'An error occurred while editing blog.')
            return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        blog_id = request.GET.get('blog_id')
        blog = Blog.objects.get(id=blog_id)
        
        return render(request, 'adminpanel/edit_blog.html', {'blog': blog})
    

@login_required
def delete_blog(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get blog by id
            blog_id = request.GET.get('blog_id')
            blog = get_object_or_404(Blog, id=blog_id)
            blog.delete()

            messages.success(request, 'Blog deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting blog: {e}")
            messages.error(request, 'An error occurred while deleting the blog.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def create_event(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    # Getting event data
    if request.method == 'POST':
        try:
            event_banner = request.FILES.get('event_banner')
            event_title = request.POST.get('event_title')
            event_offer_title = request.POST.get('event_offer_title')
            event_offer = request.POST.get('event_offer')
            sub_category_id = request.POST.get('sub_category_id')
            event_deadline_str = request.POST.get('event_deadline')
        
            # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
            event_deadline = datetime.strptime(event_deadline_str, '%Y-%m-%d')
            
            # get the category object from the category model
            event_product_category = Subcategory.objects.get(id=sub_category_id)

            event = Event.objects.create(event_banner=event_banner, event_product_category=event_product_category, event_deadline=event_deadline)      

            if event_title:
                event.event_title = event_title
            if event_offer_title:
                event.event_offer_title = event_offer_title
            if event_offer:
                event.event_offer=event_offer
            event.save()
            
            messages.success(request, 'Event Created successfully')
            return redirect('events')

        except Exception as e:
            # print(f"Error adding slider: {e}")
            messages.error(request, f"Error adding slider: {e}")
            return redirect('events')
        
    else:
        sub_categories = Subcategory.objects.all()
        return render(request, 'adminpanel/create_event.html', {'sub_categories': sub_categories})

    
@login_required
def eventsView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    events = Event.objects.all()
    return render(request, 'adminpanel/events.html', {'events': events})


@login_required
def delete_event(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get event by id
            event_id = request.GET.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            event.delete()

            messages.success(request, 'Event deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting event: {e}")
            messages.error(request, 'An error occurred while deleting the event.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_event(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    if 'cancel' in request.POST:
        # Redirect to the event list without showing the success message
        return redirect('events')    
    
    # Getting event data
    if request.method == 'POST':
        try:
            event_id = request.POST.get('event_id')
            event_banner = request.FILES.get('event_banner')
            event_title = request.POST.get('event_title')
            event_offer_title = request.POST.get('event_offer_title')
            event_offer = request.POST.get('event_offer')
            sub_category_id = request.POST.get('sub_category_id')
            event_deadline_str = request.POST.get('event_deadline')

            event = Event.objects.get(id=event_id)
            
            if event:
                if event_banner:
                    event.event_banner = event_banner
                if event_title:
                    event.event_title = event_title
                if event_offer_title:
                    event.event_offer_title = event_offer_title
                if event_offer:
                    event.event_offer=event_offer
                if sub_category_id:
                    # get the sub_category object from the sub_category model
                    event_product_category = Subcategory.objects.get(id=sub_category_id)
                    event.event_product_category = event_product_category
                if event_deadline_str:
                    # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
                    event_deadline = datetime.strptime(event_deadline_str, '%Y-%m-%d')
                    event.event_deadline = event_deadline
                event.save()

            messages.success(request, 'Event Edited successfully')
            return redirect('events')

        except Exception as e:
            # print(f"Error editing event: {e}")
            messages.error(request, f"Error editing event: {e}")
            return redirect('events')
        
    else:
        event_id = request.GET.get('event_id')
        event = Event.objects.get(id=event_id)
        sub_categories = Subcategory.objects.all()
        return render(request, 'adminpanel/edit_event.html', {'sub_categories': sub_categories, 'event': event})
    

@login_required
def event_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    event = Event.objects.get(id=request.GET.get('event_id'))
    return render(request, 'adminpanel/event_details.html', {'event': event})

@login_required
def feedbacks(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    feedbacks = Feedback.objects.all()
    return render(request, 'adminpanel/feedbacks.html', {'feedbacks': feedbacks})



@login_required
def feedback_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    feedback = Feedback.objects.get(id=request.GET.get('feedback_id'))
    return render(request, 'adminpanel/feedback_details.html', {'feedback': feedback})


@login_required
def display_feedback(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    feedback_id = request.GET.get('feedback_id')
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.is_display = True
    feedback.save()
    
    messages.success(request, 'Feedback Displayed successfully.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_feedback(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if request.method == 'GET':
        try:
            # get feedback by id
            feedback_id = request.GET.get('feedback_id')
            feedback = get_object_or_404(Feedback, id=feedback_id)
            feedback.delete()

            messages.success(request, 'Feedback deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            print(f"Error deleting feedback: {e}")
            messages.error(request, 'An error occurred while deleting the feedback.')
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def not_display_feedback(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    feedback_id = request.GET.get('feedback_id')
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.is_display = False
    feedback.save()
    
    messages.success(request, 'Feedback Not Displayed successfully.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def deal_of_the_dayView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    deals = Deal_of_the_day.objects.all()
    return render(request, 'adminpanel/deal_of_the_day_list.html', {'deals': deals})


@login_required
def add_deal_of_the_day(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            offer_price = request.POST.get('offer_price')
            deadline_str = request.POST.get('deadline')
        
            # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')

            # Creat a new deal object
            Deal_of_the_day.objects.create(product=product, offer_price=offer_price, deadline=deadline)
            
            messages.success(request, 'Deal of the Day added successfully')
            return redirect('deal_of_the_day')
            
        except Exception as e:
            messages.error(request, f'Error creating deal: {e}')
            return redirect(request.META.get('HTTP_REFERER'))
    
    products = Product.objects.all()
    return render(request, 'adminpanel/add_deal_of_the_day.html', {'products': products})


@login_required
def edit_deal_of_the_day(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the deal of the day list without showing the success message
        return redirect('deal_of_the_day')
    
    if request.method == 'POST':
        try:
            deal_id = request.POST.get('id')
            product_id = request.POST.get('product_id')
            offer_price = request.POST.get('offer_price')
            deadline_str = request.POST.get('deadline')

            # Get deal object
            deal = Deal_of_the_day.objects.get(id=deal_id)
            
            if deal:
                if product_id:
                    product = Product.objects.get(id=product_id)
                    deal.product = product
                if offer_price:
                    deal.offer_price = offer_price
                if deadline_str:
                     # Convert the date string to a datetime object (assuming 'YYYY-MM-DD' format)
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                    deal.deadline = deadline
                deal.save()
            
            messages.success(request, 'Deal of the Day edited successfully')
            return redirect('deal_of_the_day')
            
        except Exception as e:
            messages.error(request, f'Error editing deal: {e}')
            return redirect(request.META.get('HTTP_REFERER'))
    

    deal_id = request.GET.get('id')
    products = Product.objects.all()
    deal = Deal_of_the_day.objects.get(id=deal_id)
    return render(request, 'adminpanel/edit_deal_of_the_day.html', {'products': products, 'deal': deal})


@login_required
def delete_deal_of_the_day(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    if request.method == 'GET':
        try:
            # get deal by id
            deal_id = request.GET.get('id')
            deal = get_object_or_404(Deal_of_the_day, id=deal_id)
            deal.delete()

            messages.success(request, 'Deal deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            messages.error(request, (f"Error deleting deal: {e}"))
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def shop_by_dealView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    deals = shop_by_deals.objects.all()
    return render(request, 'adminpanel/shop_by_deals_list.html', {'deals': deals})


@login_required
def add_shop_by_deal(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')

    if request.method == 'POST':
        try:
            deals_name = request.POST.get('deals_name')
            deals_image = request.FILES.get('deals_image')
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id=category_id)
        
            # Creat a new deal object
            shop_by_deals.objects.create(deals_name=deals_name, delas_image=deals_image, category=category)
            
            messages.success(request, 'Deal added successfully')
            return redirect('shop_by_deal')
            
        except Exception as e:
            messages.error(request, f'Error creating deal: {e}')
            return redirect(request.META.get('HTTP_REFERER'))
    
    categories = Category.objects.all()
    return render(request, 'adminpanel/add_shop_by_deal.html', {'categories': categories})


@login_required
def edit_shop_by_deal(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the deal of the day list without showing the success message
        return redirect('deal_of_the_day')
    
    if request.method == 'POST':
        try:
            deal_id = request.POST.get('id')
            deals_name = request.POST.get('deals_name')
            deals_image = request.FILES.get('deals_image')
            category_id = request.POST.get('category_id')

            # Get deal object
            deal = shop_by_deals.objects.get(id=deal_id)
            
            if deal:
                if deals_name:
                    deal.deals_name = deals_name
                if deals_image:
                    deal.delas_image = deals_image
                if category_id:
                    category = Category.objects.get(id=category_id)
                    deal.category = category
                deal.save()
            
            messages.success(request, 'Deal edited successfully')
            return redirect('shop_by_deal')
            
        except Exception as e:
            messages.error(request, f'Error editing deal: {e}')
            return redirect(request.META.get('HTTP_REFERER'))
    

    deal_id = request.GET.get('id')
    deal = shop_by_deals.objects.get(id=deal_id)
    categories = Category.objects.all()
    return render(request, 'adminpanel/edit_shop_by_deal.html', {'categories': categories, 'deal': deal})


@login_required
def delete_shop_by_deal(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    if request.method == 'GET':
        try:
            # get deal by id
            deal_id = request.GET.get('id')
            deal = get_object_or_404(shop_by_deals, id=deal_id)
            deal.delete()

            messages.success(request, 'Deal deleted successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except Exception as e:
            messages.error(request, (f"Error deleting deal: {e}"))
            return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def ordersView(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    orders = Order.objects.all()
    return render(request, 'adminpanel/orders.html', {'orders': orders})


@login_required
def update_order(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
    if 'cancel' in request.POST:
        # Redirect to the deal of the day list without showing the success message
        return redirect('orders')
    
    if request.method == 'POST':
        try:
            order_id = request.POST.get('id')
            order_status = request.POST.get('order_status')
            order = Order.objects.get(id=order_id)
            if order_status:
                order.order_status = order_status
                order.updated_at = datetime.now()
                order.save()
                messages.success(request, 'Order updated successfully')
                return redirect('orders')
            
            messages.error(request, 'Order Staus Empty')
            return redirect('orders')
            
        except Exception as e:
            messages.error(request, f'Error updating order: {e}')
            return redirect(request.META.get('HTTP_REFERER'))

    order_id = request.GET.get('id')
    order = Order.objects.get(id=order_id)
    return render(request, 'adminpanel/update_order.html', {'order': order})


@login_required
def order_details(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
        
    order = Order.objects.get(id=request.GET.get('id'))
    return render(request, 'adminpanel/order_details.html', {'order': order})


