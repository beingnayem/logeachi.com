from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
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


