from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.views.generic import View
from products.models import Product, Subcategory
from django.contrib import messages
from django.contrib.auth.tokens  import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils import timezone
from datetime import timedelta
from accounts.utils import TokenGenerator, generate_token
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

    return render(request, 'adminpanel/admin_dashboard.html')

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
            current_site = get_current_site(request)
            email_sub = "Welcome Aboard! 🌟 Your Admin Request has been Approved!"
            message = render_to_string('adminpanel/admin_request_approve_email.html', {
                'user': user,
                'approve_by': approve_by
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
            current_site = get_current_site(request)
            email_sub = "Your Application for Admin Position at Logeachi Dot Com"
            message = render_to_string('adminpanel/admin_request_decline_email.html', {
                'user': user,
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
                current_site = get_current_site(request)
                email_sub = "Termination of Employment"
                today = timezone.now()
                effective_date = today + timedelta(days=7)
                message = render_to_string('adminpanel/remove_admin_email.html', {
                    'user': user,
                    'effective_date': effective_date
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
                current_site = get_current_site(request)
                user_first_name = user.first_name
                email_sub = 'Account Deletion Confirmation'
                message = render_to_string('adminpanel/remove_user_email.html', {
                    'user_first_name': user_first_name,
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
            
            # Get the Subcategory instance by name
            product_category = Subcategory.objects.get(id=product_category_id)
            
            # Create product
            Product.objects.create(
                product_name=product_name,
                product_image=product_image,
                product_brand=product_brand,
                product_category=product_category,
                product_price=product_price,
                product_description=product_description,
                product_quantity=product_quantity,
                product_location=product_location,
                product_warrenty=product_warrenty,
                product_cash_payment=product_cash_payment,
                product_online_payment=product_online_payment,
                product_return=product_return
            )
            
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
        
        except Exception as e:
            print(f"Error creating product: {e}")
            messages.error(request, 'An error occurred while adding the product.')
            return redirect('add_product')

    # If it's a GET request, fetch an empty list of categories
    else:
        categories = Subcategory.objects.all()
        return render(request, 'adminpanel/add_product.html', {'categories': categories})


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
            
            # current_product_warrenty = product.product_warrenty
            # current_product_cash_payment = product.product_cash_payment
            # current_product_online_payment = product.product_online_payment
            # current_product_return = product.product_return
            
            
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
            
            # Update product details and save the object in the database
            product.product_name = product_name
            if product_image:
                product.product_image = product_image
            product.product_brand = product_brand
            if product_category_id:
                product_category = get_object_or_404(Subcategory, id=product_category_id)
                product.product_category = product_category
            product.product_price = product_price
            product.product_description = product_description
            product.product_quantity = product_quantity
            product.product_location = product_location
            if product_warrenty:
            # if current_product_warrenty != product_warrenty:
                    product.product_warrenty = product_warrenty
            if product_cash_payment:
            # if current_product_cash_payment != product_cash_payment:
                    product.product_cash_payment = product_cash_payment
            if product_online_payment:
            # if current_product_online_payment != product_online_payment:
                    product.product_online_payment = product_online_payment
            if product_return:
            # if current_product_return != product_return:
                    product.product_return = product_return

            product.save()
            
            messages.success(request, 'Product edited successfully.')
            return redirect('product_list')
        
        except Exception as e:
            print(f"Error editing product: {e}")
            messages.error(request, 'An error occurred while editing the product.')
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
    
    return render(request, 'adminpanel/edit_product.html', {'categories': categories, 'product': product})


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
            
            current_site = get_current_site(request)
            email_sub = "Admin signup request"
            message = render_to_string('adminpanel/admin_signup_email.html', {
                    'domain': '127.0.0.1:8000',
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

    
