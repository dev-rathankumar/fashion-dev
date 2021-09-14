from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, RegionalManager, Business
from django.http import HttpResponse
import json
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime, timedelta, date
import datetime
import time
from .forms import UserForm, RegionalManagerForm
from django import forms
from urllib.parse import urlparse
from orders.models import Order
from plans.models import PlanOrder, Plan
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



# Custom decorator to check whether the user is regional_manager or not
def regional_manager_required(login_url=None):
    return user_passes_test(lambda u: u.is_regional_manager, login_url=login_url)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        try:
            if not user.is_regional_manager:
                messages.error(request, "This is not a regional manager's account")
                return redirect('userLogin')
        except AttributeError:
            messages.error(request, "Invalid login credentials")
            return redirect('userLogin')

        if user is not None:
            # Check for the expiry date
            rm = RegionalManager.objects.get(user__id=user.id)
            get_exp_date = rm.account_expiry_date
            exp_date = datetime.strptime(str(get_exp_date), '%Y-%m-%d')
            get_today = date.today()
            today = datetime.strptime(str(get_today), '%Y-%m-%d')
            if today > exp_date:
                messages.error(request, "Your account is expired.")
                return redirect('userLogin')
            else:
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('rm_dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('userLogin')
    return render(request, 'regional_managers/login.html')


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def dashboard(request):
    
    account_manager = RegionalManager.objects.get(user=request.user)
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        get_commission = PlanOrder.objects.filter(business=business, ordered=True)
        total_commission = 0
        for i in get_commission:
            total_commission += i.account_manager_commission
        context ={
            'account_manager': account_manager,
            'total_commission': total_commission,
        }
        return render(request, 'regional_managers/dashboard.html', context)
    except:
        return HttpResponse('<h4>Please wait until the business is assigned.</h4>')

@login_required(login_url = 'userLogin')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.warning(request, 'You are now logged out')
        return redirect('userLogin')
    return redirect('userLogin')


def forgotPassword(request):
    """Send password reset email to regional manager"""
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            if user.is_regional_manager == True:
                current_site = get_current_site(request)
                # return HttpResponse(current_site)
                mail_subject = 'Reset Your Password'
                message = render_to_string('regional_managers/reset_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.warning(request, 'Password reset link has been sent to your email address.')
                return redirect('userLogin')
            else:
                messages.warning(request, "This is not a Regional Manager's account")
                return redirect('rm_forgotPassword')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('rm_forgotPassword')
    else:
        return render(request, 'regional_managers/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    """Resetting password request validation"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('rm_resetForgotPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('rm_forgotPassword')


def rm_resetPassword(request):
    """Reset password"""
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('userLogin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('rm_resetForgotPassword')
    else:
        return render(request, 'regional_managers/resetPassword.html')


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def rm_profile(request):
    current_user = request.user
    rm = RegionalManager.objects.get(user__id=current_user.id)

    
    # account_manager = RegionalManager.objects.get(user=request.user)
    business = Business.objects.get(user__is_business=True, is_account_verified=True)
    get_commission = PlanOrder.objects.filter(business=business, ordered=True)
    total_commission = 0
    for i in get_commission:
        total_commission += i.account_manager_commission

    context = {
        'rm': rm,
        'total_commission': total_commission,
    }
    return render(request, 'regional_managers/profile.html', context)


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def rm_changePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if password == confirm_password:
            success = user.check_password(request.POST['current_password'])
            if success:
                user.set_password(password)
                user.save()
                auth.logout(request)
                messages.success(request, 'Password updated successfully. Please login again.')
                return HttpResponse('success')
            else:
                return HttpResponse('Please enter valid current password')
        else:
            return HttpResponse('Password do not match!')
    return render(request, 'regional_managers/changePassword.html')


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def editProfile(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    regionalmanager = get_object_or_404(RegionalManager, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user, prefix="user")
        regionalmanager_form = RegionalManagerForm(request.POST, prefix="regionalmanager")
        if user_form.is_valid() and regionalmanager_form.is_valid():
            user = user_form.save()
            regionalmanager_form.cleaned_data["user"] = user
            current_user = request.user
            rm = RegionalManager.objects.get(user=current_user)
            regionalmanager = regionalmanager_form.save(commit=False)
            regionalmanager.user = request.user
            regionalmanager.is_editing = True
            regionalmanager.is_verification_email_sent = True
            regionalmanager.is_account_verified = True
            regionalmanager.regional_manager_id = rm.regional_manager_id
            regionalmanager.date_of_joining = rm.date_of_joining
            regionalmanager.account_expiry_date = rm.account_expiry_date
            regionalmanager_form.save()
            messages.success(request, 'Successfully saved.')
            return redirect('/regional_managers/editProfile/'+str(pk))
        else:
            print('user form', user_form.errors)
            print('rm form', regionalmanager_form.errors)
    else:
        user_form = UserForm(instance=user, prefix="user")
        regionalmanager_form = RegionalManagerForm(instance=regionalmanager, prefix="regionalmanager")
    context = {
        'user_form': user_form,
        'regionalmanager_form': regionalmanager_form,
        'user': user,
        'regionalmanager': regionalmanager,
    }
    return render(request, 'regional_managers/editProfile.html', context)


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def supplier(request):
    
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        regional_manager = RegionalManager.objects.get(user=request.user)
    except:
        pass

    try:
        supplier = Business.objects.get(regional_manager=regional_manager, business_id=business.business_id)
        orders = Order.objects.filter(ordered=True)
        orders_count = orders.count()
        revenue = 0
        for i in orders:
            revenue += i.total
    except:
        supplier = None

    context = {
        'supplier': supplier,
        'orders_count': orders_count,
        'revenue': revenue,
    }
    return render(request, 'regional_managers/supplier.html', context)


@login_required(login_url = 'userLogin')
@regional_manager_required(login_url="userLogin")
def bizPlanPurchaseHistory(request):
    plan_orders = PlanOrder.objects.filter(ordered=True).order_by('-created_at')
    paginator = Paginator(plan_orders, 15)
    page = request.GET.get('page')
    paged_plan_orders = paginator.get_page(page)
    
    business = Business.objects.get(user__is_business=True, is_account_verified=True)
    account_expiry_date = business.account_expiry_date
    current_plan = Plan.objects.get(pk=business.plan_id)
    # Check if plan expired
    exp_date = datetime.datetime.strptime(str(account_expiry_date), '%Y-%m-%d')
    get_today = date.today()
    today = datetime.datetime.strptime(str(get_today), '%Y-%m-%d')
    if today > exp_date:
        is_expired = False
    else:
        is_expired = True
    context = {
        'plan_orders': paged_plan_orders,
        'account_expiry_date': account_expiry_date,
        'current_plan': current_plan,
        'is_expired': is_expired,
        'business': business,
    }
    return render(request, 'regional_managers/bizPlanPurchaseHistory.html', context)


def bizPlanHistoryDetail(request, pk=None):
    bizPlanHistoryDetail = get_object_or_404(PlanOrder, pk=pk)
    subtotal = bizPlanHistoryDetail.total - bizPlanHistoryDetail.tax
    context = {
        'bizPlanHistoryDetail': bizPlanHistoryDetail,
        'subtotal': subtotal,
    }
    return render(request, 'regional_managers/bizPlanHistoryDetail.html', context)
