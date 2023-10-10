from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Newsletter
from products.models import Main_Category
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
            confirm_password = request.POST['confrimpassword']
            # print(gender)
            if password != confirm_password:
                messages.error(request, "Password is not matching")
                return redirect('signup')
            
            email_exist = User.objects.filter(email=email)
            
            if not email_exist:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, password=password)
                user.is_active = False
                user.save()
                
                # Check if the user has subscribed to the newsletter
                if request.POST.get('subscribe_newsletter'):
                    SubscriberExist= Subscribers.objects.filter(email=email).exists()
                    if not SubscriberExist:
                        Subscribers.objects.create(email=email, gender=gender)
                
                # Send Activation link email
                current_domain = request.META['HTTP_HOST']
                email_sub = "Active your Logeachi Account"
                message = render_to_string('accounts/activate.html', {
                    'user': user,
                    'current_domain':current_domain,
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
    main_categories = Main_Category.objects.all()
    return render(request, 'accounts/signup.html', {'main_categories': main_categories})   


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
            current_domain = request.META['HTTP_HOST']
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
                if user.is_admin:
                    login(request, user)
                    messages.success(request, "Admin Sign in successful")
                    return redirect('admin_panel_dashboard')
                else:
                    login(request, user)
                    messages.success(request, "Sign in successful")
                    return redirect('home')
            else:
                messages.error(request, "Account not found! Incorrect e-mail or password")
                return redirect('signin')

    main_categories = Main_Category.objects.all()

    return render(request, 'accounts/signin.html', {'main_categories': main_categories})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


class RequestResetEmailView(View):
    
    def get(self, request):
        main_categories = Main_Category.objects.all()
        return render(request, 'accounts/reset-pass-request.html', {'main_categories': main_categories})

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            current_domain = request.META['HTTP_HOST']
            email_sub = 'Reset your Logeachi account Password'
            message = render_to_string('accounts/reset-pass-link.html', {
                    'current_domain': current_domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0])
                })

            email_message = EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
            EmailThread(email_message).start()
            messages.info(request, "We have sent an e-mail to reset your password")
            return redirect('signin')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        main_categories = Main_Category.objects.all()
        context = {
            'uidb64': uidb64,
            'token' : token,
            'main_categories': main_categories
        }
         
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            # print(f"user_id type: {type(user_id)}, value: {user_id}")
            user = User.objects.get(pk=user_id)
            # print(f"user type: {type(user)}, value: {user}")
            if not PasswordResetTokenGenerator().check_token(user, token):
                return render(request, 'accounts/not_valid_link.html')
            
            return render(request, 'accounts/reset-pass.html', context)
 
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            messages.error(request, "Invalid user")
            return redirect('reset-pass-request')
            
        return render(request, 'accounts/reset-pass.html', context)

    def post(self, request, uidb64, token):
        main_categories = Main_Category.objects.all()
        context = {
            'uidb64': uidb64,
            'token' : token,
            'main_categories': main_categories
        }
        
        password = request.POST['password']
        confirm_password = request.POST['confrimpassword']
        
        if password != confirm_password:
            messages.error(request, "Password and Confrim Password is not matching")
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

