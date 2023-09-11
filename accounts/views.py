from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Subscribers
# Reset password token
from django.contrib.auth.tokens  import PasswordResetTokenGenerator
# to activate account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# Generate token
from .utils import TokenGenerator, generate_token
# threading
import threading
# emails
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method=='POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            gender = request.POST['gender']
            password = request.POST['password']
            confirm_password = request.POST['confirmpassword']
            # print(gender)
            if password != confirm_password:
                messages.error(request, "Password is not matching")
                return redirect('signup')
            
            email_exist = User.objects.filter(email=email)
            
            if not email_exist:
                # Create a new user and postpone to activate the email confirmation
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, password=password)
                user.is_active = False
                user.save()
                
                # Check if the user has subscribed to the newsletter
                if request.POST.get('subscribe_newsletter'):
                    SubscriberExist= Subscribers.objects.filter(email=email).exists()
                    if not SubscriberExist:
                        Subscribers.objects.create(email=email)
                
                # Send Activation link email
                current_site = get_current_site(request)
                email_sub = "Active your Logeachi Account"
                message = render_to_string('accounts/activate.html', {
                    'user': user,
                    'domain':'127.0.0.1:8000',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                })
                email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
                EmailThread(email_message).start()
                messages.success(request, "Check email to activate your account")
                return render(request, 'accounts/signin.html')

            else:
                messages.error(request, "This e-mail is already taken")
                return redirect('signup')
            
    return render(request, 'accounts/signup.html')   

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            
            # Send Welcome email
            current_site = get_current_site(request)
            email=user.email
            email_sub = "Welcome to Logeachi.com - Your Ultimate Shopping Destination!"
            message = render_to_string('accounts/welcome_email.html', {
                'user': user,
            })
            email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
            
            messages.info(request, "Your account Acctivated successfully")
            return redirect('signin')
        
        return render(request, 'accounts/not_valid_link.html')


def signin(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method=='POST':
            email= request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Signgin successful")
                return redirect('home')

            else:
                messages.error(request, "Account not found! Incorrect e-mail or password")
                return redirect('signin')

    return render(request, 'accounts/signin.html')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'accounts/reset-pass-request.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_sub = '[Reset your Logeachi Password]'
            message = render_to_string('accounts/reset-pass-link.html', {
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0])
                })

            email_message = EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
            messages.info(request, "We have sent an e-mail to reset your password")
            return render(request, 'accounts/reset-pass-request.html')

class SetNewPasswordView(View):
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
                return render(request, 'accounts/not_valid_link.html', context)
 
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            messages.error(request, "Invalid user")
            return render(request, 'accounts/reset-pass-request.html', context)
            
        return render(request, 'accounts/reset-pass.html', context)

    def post(self, request, uidb64, token):
        
        context = {
            'uidb64': uidb64,
            'token' : token
        }
        
        password = request.POST['password']
        confirm_password = request.POST['confrimpassword']
        
        if password != confirm_password:
            messages.error(request, "Password is not matching")
            return render(request, 'accounts/reset-pass.html', context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully login with new password")
            return redirect('signin')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something went wrong")
            return render(request, 'accounts/reset-pass.html', context)
        
        return render(request, 'accounts/reset-pass.html', context)

# def showProfile(request):
#     user = request.user
#     customer_info = User.objects.filter(email=user)
#     context = {
#         'customer'  : customer_info
#     }
#     return render(request, 'accounts/profile.html', context)

# def showAddress(request):
#     user = request.user
#     address_info = Address.objects.filter(customer=user)
#     customer_info = User.objects.filter(email=user)

#     context = {
#         'address' : address_info,
#         'customer'  : customer_info
#     }
#     return render(request, 'accounts/address.html', context)

# def addAddress(request):
#     if request.method == 'POST':
#         full_name = request.POST['fullname']
#         phone = request.POST['phone']
#         city = request.POST['city']
#         thana = request.POST['thana']
#         address = request.POST['address']
#         postal_code = request.POST['postalcode']
        
#         # Get the current user
#         user = request.user
        
#         # Create a new Address object
#         new_address = Address(customer=user, full_name=full_name, phone=phone, city=city, thana=thana, postal_code=postal_code, detail_address=address)
#         new_address.save()
#         messages.success(request, "Your Address has been added")
#         # Redirect the user to the address list page
#         return redirect('show-address')
    
#     else:
#         return render(request, 'accounts/addAddress.html')

# def editAddress(request, address_id):
#     # Get the Address object to be edited
#     address = get_object_or_404(Address, pk=address_id)

#     if request.method == 'POST':
#         # Update the address with the new data from the form
#         address.full_name = request.POST.get('full_name')
#         address.phone = request.POST.get('phone')
#         address.city = request.POST.get('city')
#         address.thana = request.POST.get('thana')
#         address.detail_address = request.POST.get('detail_address')
#         address.postal_code = request.POST.get('postal_code')
#         address.save()
#         messages.success(request, "Your Address has been Updated")
#         # Redirect the user to the address list page
#         return redirect('show-address')

#     # Render the edit address form with the current data from the address object
#     return render(request, 'accounts/editAddress.html', {'address': address})

# def deleteAddress(request, address_id):
#     address = get_object_or_404(Address, pk=address_id)
#     if address:
#         address.delete()
#         messages.success(request, "Your Address has been Deleted")
#         return redirect('show-address')
    
#     else:
#         messages.error(request, "No Address")
#         return redirect('show-address')