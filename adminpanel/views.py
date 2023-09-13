from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from products.models import Product, Subcategory
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from datetime import timedelta
# emails
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings
from accounts.views import EmailThread
from django.template.loader import render_to_string

# Create your views here.



@login_required
def adminPanelView(request):
    if request.user.is_admin:
        return render(request, 'adminpanel/admin_dashboard.html')
    else:
        return render(request, 'accounts/wrong_path.html')
    
@login_required
def team_memberView(request):
    if request.user.is_admin:
        team_members= User.objects.filter(is_admin=True)
        # print('=========================================================', team_members)
        return render(request, 'adminpanel/team_member.html', {'team_members': team_members})

        return render(request, 'accounts/wrong_path.html')

@login_required
def admin_request(request):
    id= request.user.id
    email= request.user.email
    user= User.objects.get(id=id, email=email)
    if user:
        if user.admin_request==None:
            user.admin_request='requested'
            user.save()
            # print('=========================================================', user.admin_request)
            # print('=========================================================', user.email)
            messages.success(request, 'Request sent successfully to admin panel')
            return redirect('home')
        else:
            # print('=========================================================', user.admin_request)
            # print('=========================================================', user.email)
            messages.error(request, 'Request already sent to admin panel')
            return redirect('home')
    else:
        messages.error(request, 'User not found')
        return redirect('home')
    
    return redirect('home')

@login_required
def admin_request_listView(request):
    if request.user.is_admin:
        admin_requests = User.objects.filter(admin_request='requested')
        # print('=========================================================', admin_requests)
        return render(request, 'adminpanel/admin_request_list.html', {'admin_requests': admin_requests})

        return render(request, 'accounts/wrong_path.html')
 
@login_required
def admin_request_approve(request):
    if request.user.is_admin:
        if request.method == 'POST':
            id = request.POST.get('id')
            email = request.POST.get('email')
            approve_by = request.user
            try:
                user = User.objects.get(id=id, admin_request='requested')
                # print('=========================================================', user)
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
    
    return render(request, 'accounts/wrong_path.html')

@login_required
def admin_request_decline(request):
    if request.user.is_admin:
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
    
    return render(request, 'accounts/wrong_path.html')

@login_required
def remove_admin(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        # print('================================================================', email)
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
    if request.user.is_admin:
        customers= User.objects.filter(is_admin=False)
        # print('=========================================================', customers)
        return render(request, 'adminpanel/customer_list.html', {'customers': customers})

        return render(request, 'accounts/wrong_path.html')
    
@login_required
def productView(request):
    if request.user.is_admin:
        products= Product.objects.all()
        return render(request, 'adminpanel/product_list.html', {'products': products})

    return render(request, 'accounts/wrong_path.html')


@login_required
def add_product(request):
    if request.user.is_admin:
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
            # print("============================================================", categories[0])
            return render(request, 'adminpanel/add_product.html', {'categories': categories})
    
    return render(request, 'accounts/wrong_path.html')


@login_required
def edit_product(request):
    if not request.user.is_admin:
        return render(request, 'accounts/wrong_path.html')
    
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
            
            # Get the Subcategory instance by ID
            product_category = get_object_or_404(Subcategory, id=product_category_id)
            print("before Updating the produc=========================", product.product_warrenty)
            print("after edit in html =================================", product_warrenty)
            
            # Update product details and save the object in the database
            product.product_name = product_name
            if product_image:
                product.product_image = product_image
            product.product_brand = product_brand
            product.product_category = product_category
            product.product_price = product_price
            product.product_description = product_description
            product.product_quantity = product_quantity
            product.product_location = product_location
            product.product_warrenty = product_warrenty
            product.product_cash_payment = product_cash_payment
            product.product_online_payment = product_online_payment
            product.product_return = product_return
            product.save()
            
            print("After Updateing the product ========================", product.product_warrenty)
            
            messages.success(request, 'Product edited successfully.')
            return redirect('product_list')
        
        except Exception as e:
            print(f"Error editing product: {e}")
            messages.error(request, 'An error occurred while editing the product.')
            return redirect('product_list')
    
    product_id = request.GET.get('id')
    product =Product.objects.get(id=product_id)
    
    # If it's a GET request, fetch the list of categories and render the edit form
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