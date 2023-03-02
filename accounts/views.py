from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            password = request.POST['password']
            confirm_password = request.POST['confirmpassword']

            if password != confirm_password:
                messages.error(request, "Password is not matching")
                return redirect('signup')
            
            
            email_exist = User.objects.filter(email=email)
            
            if not email_exist:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
                user.is_active = False
                user.save()
                
                current_site = get_current_site(request)
                email_sub = "Active your Logeachi Account"
                message = render_to_string('activate.html', {
                    'user': user,
                    'domain':'127.0.0.1:8000/',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                })

                email_message= EmailMessage(email_sub, message, settings.EMAIL_HOST_USER, [email],)
                EmailThread(email_message).start()
                
                # messages.info(request, "Your Account Created successfully")
                
                messages.success(request, "An e-mail has been sent to your account, active your account throw the link in e-mail")
                return render(request, 'signin.html')
            
            else:
                messages.error(request, "This e-mail is already taken")
                return redirect('signup')
            
    return render(request, 'signup.html')   


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
            messages.info(request, "Your Account Acctivated successfully")
            return redirect('signin')
        
        return render(request, 'activatefail.html')


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
                messages.success(request, "Login successful")
                return redirect('home')
            
            else:
                messages.error(request, "Account not found! Incorrect e-mail or password")
                return redirect('signin')
            
    return render(request, 'signin.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')