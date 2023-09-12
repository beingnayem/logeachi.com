from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
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
        if user.admin_request=='':
            user.admin_request='requested'
            user.save()
            messages.success(request, 'Request sent successfully to admin panel')
            return redirect('home')
        else:
            messages.error(request, 'Request already sent to admin panel')
            return redirect('home')
    else:
        messages.error(request, 'User not found')
        return redirect('home')
    
    return redirect('home')


@login_required
def admin_requestsView(request):
    if request.user.is_admin:
        approve_requests= User.objects.filter(admin_request='requested')
        # print('=========================================================', approve_requests)
        return render(request, 'adminpanel/admin_approve_requests.html', {'approve_requests': approve_requests})

        return render(request, 'accounts/wrong_path.html')
    
    
    
@login_required
def admin_request_approveView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            user = User.objects.get(id=id, admin_request='requested')
            # print('=========================================================', user)
            user.is_active = True
            user.is_admin= True
            user.admin_request='approved'
            user.save()
            messages.success(request, 'Admin request approve succesfull')
            return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('admin_request_list')


@login_required
def admin_request_declineView(request, id):
    user = get_object_or_404(User, id=id)
    
    if user is not None:
        user.delete()
        messages.success(request, 'User removed succesfull')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'User not found')
        return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect('admin_request_list')

@login_required
def remove_adminView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            user = User.objects.get(id=id, is_admin=True)
            if not user.email==request.user.email:
                user.is_active = True
                user.is_admin= False
                user.admin_request=''
                user.save()
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
def remove_userView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            user = User.objects.get(id=id)
            if not user.email==request.user.email:
                user.delete()
                messages.success(request, 'User Remove succesfull')
                return redirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, 'Current admin can not remove himself')
                return redirect(request.META.get('HTTP_REFERER'))
        
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('team_member')


