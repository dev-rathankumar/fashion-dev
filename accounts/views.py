from portfolio.models import PortfolioActivation, PortfolioHeader
from blogs.models import BlogActivation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import DashboardImage, User, RegionalManager, Business, Customer
from contacts.models import Inquiry
from products.models import Product, ProductActivation, SalesPopupSetting
from orders.models import Order, OrderProduct, StoreLocation
from business.models import PaymentSetting

# Send account verification email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserForm

from django.http import HttpResponse
from urllib.parse import urlparse
from sitesettings.models import CashOnDelivery, DirectDepositEmail, Homepage, ParallaxBackground, Header, ContactPage, Footer, AboutPage, PaypalConfig, Policy, ServiceActivation, TermsAndCondition, Topbar
from emails.models import BusinessEmailSetting
from datetime import date, datetime
import time
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.
def userRegister(request):
    """User Registration"""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']


        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('userRegister')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('userRegister')
                else:
                    user = User.objects.create_user(first_name=first_name,
                    last_name=last_name, username=username, email=email, password=password)
                    user.is_customer = True
                    user.profile_picture="default/default-user.png"
                    user.save()
                    current_site = get_current_site(request)
                    business = Business.objects.get(domain_name=current_site.domain)
                    header = Header.objects.get(business=business)
                    footer = get_object_or_404(Footer, business=business)
                    footer_text = footer.footer_text
                    support_email = business.user.email

                    # print('business', )
                    # print('header',header.site_logo)
                    # return HttpResponse('Stopping code')
                    # Send account verification email

                    mail_subject = 'Activate your account.'
                    message = render_to_string('accounts/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'header': header,
                        'support_email': support_email,
                        'footer':footer,
                        'footer_text':footer_text,
                    })
                    to_email = email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.content_subtype = "html"
                    email.send()
                    messages.warning(request, 'Please confirm your email address to complete the registration')
                    return redirect('userLogin')
        else:
            messages.error(request, 'Password do not match')
            return redirect('userRegister')
    else:
        return render(request, 'accounts/userRegister.html')


def activate(request, uidb64, token):
    """Activating Users"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Automatically Create Customer
        customer = Customer()
        customer.user = user
        customer.save()


        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('userLogin')
    else:
        messages.error(request, 'Activation link is invalid')
        return redirect('userRegister')


def userLogin(request):
    """User Login"""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                if user.is_business:
                    auth.login(request, user)
                    messages.success(request, "You are now logged in!")
                    return redirect('biz_dashboard')

                elif user.is_regional_manager:
                    auth.login(request, user)
                    messages.success(request, "You are now logged in!")
                    return redirect('rm_dashboard')
                elif user.is_superadmin:
                    auth.login(request, user)
                    messages.success(request, "You are now logged in!")
                    return redirect('userDashboard')
                else:
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return redirect('userDashboard')
            except:
                pass
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('userLogin')
    return render(request, 'accounts/userLogin.html')


@login_required(login_url='/userLogin')
def userDashboard(request):
    user_inquiry = Inquiry.objects.order_by('-create_date').filter(user_id=request.user.id)
    inquiry_count = user_inquiry.count()


    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, ordered=True)
    orders_count = orders.count()

    context = {
        'inquiry_count' : inquiry_count,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/userDashboard.html', context)

@login_required(login_url='/userLogin')
def editUser(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved.')
            return redirect('/userDashboard/user/edit/'+str(pk))
    else:
        form = UserForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'accounts/editUser.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect('userLogin')
    return redirect('home')


def forgotPassword(request):
    """Send password reset email"""
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            current_site = get_current_site(request)
            business = Business.objects.get(domain_name=current_site.domain)
            header = Header.objects.get(business=business)
            footer = get_object_or_404(Footer, business=business)
            footer_text = footer.footer_text
            support_email= business.user.email
            footer = Footer.objects.get(business=business)
            footer_credit = footer.footer_text

            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'header': header,
                'support_email':support_email,
                'footer' : footer,
                'footer_credit': footer_credit,

            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            messages.warning(request, 'Password reset link has been sent to your email address.')
            return redirect('userLogin')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    else:
        return render(request, 'accounts/forgotPassword.html')


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
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('userLogin')


def resetPassword(request):
    """Reset password"""
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            if user.is_customer == True and user.is_active == False:
                user.is_active = True
                # Automatically Create Customer
                customer = Customer()
                customer.user = user
                customer.save()
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('userLogin')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


# Regional Manager Activation Validation
def rm_password_reset_validate(request, uidb64, token):
    """Regional Manager Resetting password request validation"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('rm_password_reset')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('home')

# Regional Manager Activation
def rm_password_reset(request):
    """Reset password"""
    if request.method == 'POST':
        rm_id = request.session['uid']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.get(pk=rm_id)
            regional_manager = RegionalManager.objects.get(user=user)
            user.set_password(password)
            user.is_regional_manager = True
            user.is_active = True
            regional_manager.is_account_verified = True
            user.save()
            regional_manager.save()
            mail_subject = 'Your Account is Activated'
            # message = 'Congratulations! Your account has been activated.'
            current_site = get_current_site(request)
            message = render_to_string('accounts/rm_acc_activated_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, 'Congratulations! Your account has been activated.')
            return redirect('userLogin')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('rm_password_reset')
    else:
        return render(request, 'accounts/rm_password_reset.html')


# Business Activation Validation
def biz_password_reset_validate(request, uidb64, token):
    """Business Resetting password request validation"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('biz_password_reset')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('biz_login')

# Business Activation
def biz_password_reset(request):
    """Reset password"""
    if request.method == 'POST':
        biz_id = request.session['uid']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.get(pk=biz_id)
            business = Business.objects.get(user=user)
            user.set_password(password)
            user.is_business = True
            user.is_active = True
            business.is_account_verified = True
            user.save()
            business.save()

            # Automatically creating homepage for this business
            homepage = Homepage()
            homepage.business = business
            homepage.save()

            # Automatically Creating Parallax Background Image for Homepage
            background = ParallaxBackground()
            background.homepage = homepage
            background.save()

            # Automatically Creating Payment Setting
            payment_setting = PaymentSetting()
            payment_setting.user_id = user.id
            payment_setting.business = business
            payment_setting.save()

            # Automatically Creating Email Setting
            email_setting = BusinessEmailSetting()
            email_setting.business = business
            email_setting.save()

            # Automatically creating footer
            header = Header()
            header.business = business
            header.site_title = 'Your Website Title Here'
            header.save()

            # Automatically creating footer
            footer = Footer()
            footer.business = business
            footer.save()

            # Automatically creating topbar
            topbar = Topbar()
            topbar.business = business
            topbar.save()

            # Automatically creating about us page
            about_page = AboutPage()
            about_page.heading = 'About Us'
            about_page.business = business
            about_page.cover_image = 'default/about-img.jpg'
            about_page.save()

            # Automatically Creating Contact Page
            contact_page = ContactPage()
            contact_page.business = business
            contact_page.address_line_1 = business.address_line_1
            contact_page.address_line_2 = business.address_line_2
            contact_page.city = business.city
            contact_page.pin_code = business.pin_code
            contact_page.country = business.country
            contact_page.state = business.state
            contact_page.phone_number = business.user.phone_number
            contact_page.email = business.user.email
            contact_page.save()

            # Automatically creating Privacy Policy page
            policy = Policy()
            policy.heading = 'Privacy Policy'
            policy.business = business
            policy.save()

            # Automatically creating Terms & Conditions page
            terms = TermsAndCondition()
            terms.heading = 'Terms & Conditions'
            terms.business = business
            terms.save()

            # Automatically creating Direct deposit email entry
            ddEmail = DirectDepositEmail()
            ddEmail.business = business
            ddEmail.save()

            # Automatically creating dashboard images entry
            dashImage = DashboardImage()
            dashImage.business = business
            dashImage.business_landing_image = 'default/dashboard-landing-image.jpg'
            dashImage.account_manager_landing_image = 'default/dashboard-landing-image.jpg'
            dashImage.save()
            # Automatically creating Paypal Config entry
            ppConfig = PaypalConfig()
            ppConfig.business = business
            ppConfig.save()

            # Automatically creating Blog Activation entry
            blog_activation = BlogActivation()
            blog_activation.business = business
            blog_activation.save()

            # Automatically creating Product Activation entry
            product_activation = ProductActivation()
            product_activation.business = business
            product_activation.save()

            # Automatically creating Service Activation entry
            service_activation = ServiceActivation()
            service_activation.business = business
            service_activation.save()

            # Automatically creating Portfolio Header entry
            portfolio_header = PortfolioHeader()
            portfolio_header.business = business
            portfolio_header.heading = 'Our Portfolio'
            portfolio_header.save()

            # Automatically creating Portfolio Activation entry
            portfolio_activation = PortfolioActivation()
            portfolio_activation.business = business
            portfolio_activation.save()

            # Automatically creating Paypal Config entry
            codConfig = CashOnDelivery()
            codConfig.business = business
            codConfig.save()

            # Automatically creating Store Location entry
            store_location = StoreLocation()
            store_location.business = business
            store_location.store_name = business.company_name
            store_location.phone_number = business.user.phone_number
            store_location.email = business.user.email
            store_location.address_line_1 = business.address_line_1
            store_location.address_line_2 = business.address_line_2
            store_location.city = business.city
            store_location.pin_code = business.pin_code
            store_location.country = business.country
            store_location.state = business.state
            store_location.save()

            # Automatically creating Popup settings
            popup_settings = SalesPopupSetting()
            popup_settings.business = business
            popup_settings.background_color = '#37384E'
            popup_settings.text_color = '#FFFFFF'
            popup_settings.notification_position = 'Left Bottom Corner'
            popup_settings.notification_style = 'Rectangled'
            popup_settings.save()

            mail_subject = 'Your Business Account is Activated'
            # message = 'Congratulations! Your business account has been activated.'
            current_site = get_current_site(request)
            message = render_to_string('accounts/biz_acc_activated_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, 'Congratulations! Your account has been activated.')
            return redirect('userLogin')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('biz_password_reset')
    else:
        return render(request, 'accounts/biz_password_reset.html')


@login_required(login_url='/userLogin')
def userInquiry(request):
    user_inquiry = Inquiry.objects.order_by('-create_date').filter(user_id=request.user.id)
    paginator = Paginator(user_inquiry, 10)
    page = request.GET.get('page')
    paged_user_inquiry = paginator.get_page(page)
    context = {
            'inquiries': paged_user_inquiry,
        }
    return render(request, 'accounts/inquiries.html', context)

@login_required(login_url='/userLogin')
def changeuserPassword(request):
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
                return redirect('changeuserPassword')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('changeuserPassword')
        else:
            messages.error(request, 'Passwords do not match!')
    return render(request, 'accounts/changeuserPassword.html')


@login_required(login_url='/userLogin')
def myOrders(request):
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
            'orders': paged_orders,
        }
    return render(request, 'accounts/myorders.html', context)


def orderDetail(request, pk=None):
    order_detail = OrderProduct.objects.filter(order__order_number=pk)
    order = Order.objects.get(order_number=pk)
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/orderDetail.html', context)

# def supplier(request):
#     url = request.build_absolute_uri()
#     domain = urlparse(url).netloc
#     business = Business.objects.get(domain_name=domain)
#     regional_manager = RegionalManager.objects.get(user=request.user)
#
#     try:
#         supplier = Business.objects.get(regional_manager=regional_manager, business_id=business.business_id)
#     except:
#         supplier = None
#
#     context = {
#         'supplier': supplier,
#     }
#     return render(request, 'regional_managers/supplier.html', context)
