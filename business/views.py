from portfolio.models import Portfolio, PortfolioActivation, PortfolioGallery
from sitesettings.models import Service, ServiceActivation
from orders.views import orderproduct
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User, Customer, RegionalManager
from accounts.models import Business, TaxOnPlan
from django.http import HttpResponse, JsonResponse
from .forms import AttributeValueForm, PaymentSettingForm, PortfolioForm, PortfolioGalleryForm, ProductAttributeForm, ServiceForm
from .models import PaymentSetting
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from datetime import datetime, timedelta, date
# import datetime
import time
import json
from django.contrib import messages
from .forms import UserForm, BusinessForm, ProductForm, ProductGalleryForm, ProductVariantForm, BlogForm,BlogCategoryForm
from .forms import CategoryForm, OrderForm, TaxSettingForm, ColorForm, SizeForm
from products.models import AttributeValue, Product, ProductActivation, ProductAttribute, ProductGallery, Variants, ReviewRating, Color, Size
from django.forms import inlineformset_factory
from django import forms
from django.template.defaultfilters import slugify
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from orders.models import Order, OrderProduct
from plans.models import Plan, PlanOrder, PlanPayment
import json
import ast # for converting tax_data string to dict
from django.template.loader import render_to_string
from carts.models import TaxSetting, Tax
from sitesettings.forms import HeaderForm
from contacts.models import Inquiry, SiteContact
from urllib.parse import urlparse
from blogs.models import Blog, BlogActivation, Comment
from blogs.models import Category as BlogCategory
from django.db.models import Sum, Min, Count, Q


# Custom decorator to check if the business account expired or not
def is_account_expired(func):
    def wrapper(request, *args, **kwargs):
        try:
            business = Business.objects.get(user__is_business=True, is_account_verified=True)
            get_exp_date = business.account_expiry_date
            exp_date = datetime.strptime(str(get_exp_date), '%Y-%m-%d')
            get_today = date.today()
            today = datetime.strptime(str(get_today), '%Y-%m-%d')

            if today > exp_date:
                messages.error(request, "Your account is expired!")
                return redirect('biz_dashboard')
        except:
            pass
        return func(request, *args, **kwargs)
    return wrapper




# Custom decorator to check whether the user is business or not
def business_required(login_url=None):
    return user_passes_test(lambda u: u.is_business, login_url=login_url)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        try:
            if not user.is_business:
                messages.error(request, "This is not a business account")
                return redirect('userLogin')
        except AttributeError:
            messages.error(request, "Invalid login credentials")
            return redirect('userLogin')

        if user is not None:
            # Check for the expiry date
            biz = Business.objects.get(user__id=user.id)
            get_exp_date = biz.account_expiry_date
            exp_date = datetime.strptime(str(get_exp_date), '%Y-%m-%d')
            get_today = date.today()
            today = datetime.strptime(str(get_today), '%Y-%m-%d')
            if today > exp_date:
                messages.error(request, "Your account is expired.")
                return redirect('userLogin')
            else:
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('biz_dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('userLogin')
    return render(request, 'business/login.html')


@login_required(login_url = 'userLogin')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('userLogin')
    return redirect('userLogin')



@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def dashboard(request):
    orders = Order.objects.filter(Q(ordered=True) & ~Q(status='Cancelled'))
    orders_count = orders.count()
    revenue = 0
    for i in orders:
        revenue += i.total
        revenue = round(revenue,2)
    products = Product.objects.all()
    products_count = products.count()
    customers = User.objects.filter(is_customer=True, is_active=True)
    customers_count = customers.count()
    inquiries = Inquiry.objects.all()
    inquiries_count = inquiries.count()
    context = {
        'orders_count': orders_count,
        'revenue': revenue,
        'products_count': products_count,
        'customers_count': customers_count,
        'inquiries_count': inquiries_count,
    }
    return render(request, 'business/dashboard.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def biz_profile(request):
    current_user = request.user
    biz = Business.objects.get(user__id=current_user.id)
    orders = Order.objects.filter(Q(ordered=True) & ~Q(status='Cancelled'))
    orders_count = orders.count()
    revenue = 0
    for i in orders:
        revenue += i.total
        revenue = round(revenue,2)
    context = {
        'biz': biz,
        'revenue': revenue,
        'orders_count': orders_count,
    }
    return render(request, 'business/profile.html', context)

@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def biz_changePassword(request):
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
            return HttpResponse('Passwords do not match!')
    return render(request, 'business/changePassword.html')


def forgotPassword(request):
    """Send password reset email to Business"""
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            if user.is_business == True:
                current_site = get_current_site(request)
                # return HttpResponse(current_site)
                mail_subject = 'Reset Your Password'
                message = render_to_string('business/reset_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
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
                messages.warning(request, "This is not a Business account")
                return redirect('biz_forgotPassword')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('biz_forgotPassword')
    else:
        return render(request, 'business/forgotPassword.html')

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
        return redirect('biz_resetForgotPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('biz_forgotPassword')

def biz_resetPassword(request):
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
            return redirect('biz_resetForgotPassword')
    else:
        return render(request, 'business/resetPassword.html')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editProfile(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    business = get_object_or_404(Business, pk=pk)
    orders = Order.objects.filter(Q(ordered=True) & ~Q(status='Cancelled'))

    orders_count = orders.count()
    revenue = 0
    for i in orders:
        revenue += i.total
        revenue =round(revenue,2)
    # plan = get_object_or_404(Business, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user, prefix="user")
        business_form = BusinessForm(request.POST, prefix="business")

        if user_form.is_valid() and business_form.is_valid():
            user = user_form.save()
            business_form.cleaned_data["user"] = user
            current_user = request.user
            biz = Business.objects.get(user=current_user)
            business = business_form.save(commit=False)
            business.user = request.user
            business.plan_id = biz.plan.id
            business.is_editing = True
            business.is_verification_email_sent = True
            business.is_account_verified = True
            business.business_id = biz.business_id
            business.domain_name = biz.domain_name
            business.account_activation_date = biz.account_activation_date
            business.account_expiry_date = biz.account_expiry_date
            business.regional_manager = biz.regional_manager
            business.created_date = biz.created_date
            #biz.account_expiry_date = True
            business_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('/business/editProfile/'+str(pk))
        else:
            print('user form', user_form.errors)
            print('rm form', business_form.errors)
    else:
        user_form = UserForm(instance=user, prefix="user")
        business_form = BusinessForm(instance=business, prefix="business")

    context = {
        'user_form': user_form,
        'business_form': business_form,
        'user': user,
        'business': business,
        'orders_count':orders_count,
        'revenue':revenue,
    }
    return render(request, 'business/editProfile.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def paymentSettings(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    pay_setting = get_object_or_404(PaymentSetting, user=user)
    if request.method == 'POST':
        form = PaymentSettingForm(request.POST, instance=pay_setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your payment settings are saved successfully.')
            return redirect('/business/paymentSettings/'+str(pk))
    else:
        form = PaymentSettingForm(instance=pay_setting)

    context = {
        'form': form,
    }
    return render(request, 'business/paymentSettings.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allProducts(request):
    business = get_object_or_404(Business, pk=request.user.id)
    products = Product.objects.filter(business=business).order_by('-created_date')
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # get blog activation status
    product_activation = ProductActivation.objects.get(business=business)

    context = {
        'products': paged_products,
        'product_activation': product_activation,
    }
    return render(request, 'business/allProducts.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editProduct(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        basicInfo_form = ProductForm(request.POST, request.FILES, instance=product)
        if basicInfo_form.is_valid():
            product_name = basicInfo_form.cleaned_data['product_name']
            makeSlug = product_name + str(pk)
            product.slug = slugify(makeSlug)
            basicInfo_form.save()
            return redirect('/business/products/editProduct/'+str(pk)+'/editGallery/')
        else:
            print(basicInfo_form.errors)

    else:
        basicInfo_form = ProductForm(instance=product)
    context = {
        'basicInfo_form': basicInfo_form,
        'product': product,
    }
    return render(request, 'business/editProduct.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editGallery(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    ProductGalleryFormSet = inlineformset_factory(Product, ProductGallery, form=ProductGalleryForm, extra=1)

    if request.method == 'POST':
        add_another = request.POST['add_another']
        formset = ProductGalleryFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            if add_another == 'true':
                return redirect('/business/products/editProduct/'+str(pk)+'/editGallery/')
            elif add_another == 'finish':
                product.is_active = True
                product.save()
                messages.success(request, 'Product has been uploaded successfully.')
                return redirect('allProducts')
            else:
                return redirect('/business/products/editProduct/'+str(pk)+'/editVariants/')
        else:
            return HttpResponse(formset.errors)
    else:
        formset = ProductGalleryFormSet(instance=product)
        # print('gallery image count', len(formset))
    context = {
        'product' : product,
        'formset': formset,
    }
    return render(request, 'business/editGallery.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editVariants(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    ProductVariantFormSet = inlineformset_factory(Product, Variants, form=ProductVariantForm, extra=1)

    # Check if gellery image is 0, return back to edit gallery
    chkGallery = ProductGallery.objects.filter(product=product)
    if chkGallery.count() <= 0:
        url = request.META.get('HTTP_REFERER')
        messages.error(request, 'You have deleted the image. Add atleast one image in the gallery')
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        add_another = request.POST['add_another']
        # pr_attrs = [name for name in request.POST.keys() if name.endswith('-product_attribute')]
        # attr = []
        # for i in pr_attrs:
        #     # attr.append(i)
        #     att_name = request.POST.getlist(i)
        #     attr.append(att_name)

        # attr_vals = [name for name in request.POST.keys() if name.endswith('-attribute_value')]
        # att_values = []
        # for i in attr_vals:
        #     # attr.append(i)
        #     att_val = request.POST.getlist(i)
        #     att_values.append(att_val)
        # # print(attr_val)
        
        # # attr = request.POST.getlist('variants_set-0-product_attribute')
        # # print('attr==>', attr)
        # # att_values = request.POST.getlist('variants_set-0-attribute_value')
        # # print('att_values==>', att_values)
        
        # if attr != [''] and att_values != ['']:
        #     attr_names = []
        #     for i in attr:
        #         for j in i:
        #             attr_name = ProductAttribute.objects.get(id=j)
        #             attr_names.append(attr_name.attribute_name)
        #     print('attr_names==>', attr_names)
        #     attr_values = []
        #     for i in att_values:
        #         for j in i:
        #             attr_val = AttributeValue.objects.get(id=j)
        #             attr_values.append(attr_val.attribute_value)
        #     print('attr_values==>', attr_values)
            
            # print('res==>', res)
        formset = ProductVariantFormSet(request.POST, instance=product)
        if formset.is_valid():
            # if attr != [''] and att_values != ['']:
            #     new = formset.save(commit=False)
            #     for n in new:
            #         res = dict(zip(attr_names, attr_values))
            #         print('res==>', res)
            #         n.variant_data = res
            #         n.save()
            # else:
            formset.save()
            
            product.is_active = True
            product.save()
            if add_another == 'true':
                return redirect('/business/products/editProduct/'+str(pk)+'/editVariants/')
            else:
                variants = Variants.objects.filter(product=product)
                total_quantity = variants.aggregate(Sum('quantity'))['quantity__sum'] or 0
                min_price = variants.aggregate(Min('price'))['price__min'] or 0.00
                product.price = min_price
                product.stock = total_quantity
                product.save()
                messages.success(request, 'Product has been uploaded successfully.')
                return redirect('allProducts')
        else:
            return HttpResponse(formset.errors)
    else:
        # Get the value of variant from the product model. Based on that show/hide color and size
        command = ''
        message1 = ''
        message2 = ''
        
        if product.variant == 'Color':
            command = 'delete_size'
            message1 = 'Product with only Color variant.'
            message2 = 'Add Size too.'
        elif product.variant == 'Size':
            command = 'delete_color'
            message1 = 'Product with only Size variant.'
            message2 = 'Add Color too.'
        elif product.variant == 'Size-Color':
            message1 = 'Product with Size and Color variant.'
            message2 = 'Change Variants.'
        elif product.variant == 'Custom':
            command = 'delete_size_color'
        formset = ProductVariantFormSet(instance=product)
        gallery = ProductGallery.objects.filter(product=product)

    context = {
        'product' : product,
        'formset': formset,
        'gallery': gallery,
        'command': command,
        'message1': message1,
        'message2': message2,
    }
    return render(request, 'business/editVariants.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addProduct(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        basicInfo_form = ProductForm(request.POST, request.FILES)
        if basicInfo_form.is_valid():
            current_user = request.user
            business_name = Business.objects.get(user=current_user)
            product_name = basicInfo_form.cleaned_data['product_name']
            product = basicInfo_form.save(commit=False)
            product.business = business_name
            basicInfo_form.save()
            pk = product.id
            makeSlug = product_name + str(pk)
            product.slug = slugify(makeSlug)
            product.save()
            return redirect('/business/products/editProduct/'+str(pk)+'/editGallery/')
        else:
            print(basicInfo_form.errors)
            messages.error(request, 'Something went wrong! Please try again.')
            return HttpResponseRedirect(url)
    else:
        basicInfo_form = ProductForm()
    context = {
        'basicInfo_form': basicInfo_form,
    }

    return render(request, 'business/addProduct.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteProduct(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product has been deleted successfully.')
    return redirect('allProducts')



# Manage Categories
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allCategories(request):
    categories = Category.objects.filter(is_active=True).order_by('-created_date')
    context = {
        'categories': categories,
    }
    return render(request, 'business/allCategories.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Added Successfully')
            return redirect('addCategory')
        else:
            print(form.errors)

    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addCategory.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Modified Successfully')
            return redirect('allCategories')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'business/editCategory.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted.')
    return redirect('allCategories')


# Manage Orders
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allOrders(request):
    orders = Order.objects.filter(ordered=True).order_by('-created_at')
    paginator = Paginator(orders, 15)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        'orders': paged_orders,
    }
    return render(request, 'business/allOrders.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def bizOrderDetail(request, pk=None):
    try:
        order = Order.objects.get(order_number=pk)
        ordered_products = OrderProduct.objects.filter(order__order_number=pk)
    except Order.DoesNotExist:
        return redirect('allOrders')
    subtotal = 0
    for i in ordered_products:
        if i.product.variant == 'None':
            subtotal += i.product.price * i.quantity
        else:
            subtotal += i.variant.price * i.quantity

    context = {
        'ordered_products': ordered_products,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'business/viewOrder.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editOrder(request, pk=None):
    url = request.META.get('HTTP_REFERER')
    order = get_object_or_404(Order, pk=pk)
    # Get ordered products
    try:
        ordered_products = OrderProduct.objects.filter(order__order_number=order.order_number)
        subtotal = 0
        for i in ordered_products:
            if i.product.variant == 'None':
                subtotal += i.product.price * i.quantity
            else:
                subtotal += i.variant.price * i.quantity
    except Order.DoesNotExist:
        return redirect('allOrders')
    current_status = order.status
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            changed_status = form.cleaned_data['status']
            if changed_status != current_status:
                # Send order update email
                message = ''
                if changed_status == 'New':
                    message = 'Your order status has been set to New'
                elif changed_status == 'On Hold':
                    message = 'Your order is on Hold'
                elif changed_status == 'Accepted':
                    message = 'Congrats! Your order has been accepted'
                elif changed_status == 'Completed':
                    message = 'Thank you! Your order has been completed.'
                elif changed_status == 'Cancelled':
                    # Reduce quantity of sold products from the product db
                    for item in ordered_products:
                        product = Product.objects.get(id=item.product_id)
                        product.stock += item.quantity
                        product.save()
                        variants = Variants.objects.filter(id=item.variant_id)
                        for var in variants:
                            var.quantity += item.quantity
                            var.save()
                    message = 'We are sorry! Your order has been cancelled.'
                else:
                    message = 'Your order has been set to '+changed_status

                mail_subject = message
                # current_site = get_current_site(request)
                message = render_to_string('orders/order_status_email.html', {
                    'user': order.user,
                    # 'domain': current_site.domain,
                    'changed_status': changed_status,
                    'order': order,
                    'message': message,
                })
                to_email = order.user.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                    
                )
                email.content_subtype = "html"
                email.send()
                # print('Current status was '+current_status +', '+ 'new status is '+ changed_status)
            form.save()
            messages.success(request, 'Order has been updated.')
            return HttpResponseRedirect(url)
        else:
            print(form.errors)

    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
        'order': order,
        'ordered_products': ordered_products,
        'subtotal': subtotal,
    }
    return render(request, 'business/editOrder.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteOrder(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, 'Order has been deleted.')
    return redirect('allOrders')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def plans(request):
    plans = Plan.objects.all().order_by('plan_price')
    business = Business.objects.get(user=request.user)
    account_expiry_date = business.account_expiry_date
    current_plan = Plan.objects.get(pk=business.plan_id)
    context = {
        'plans': plans,
        'current_plan': current_plan,
        'account_expiry_date': account_expiry_date,
    }
    return render(request, 'business/plans.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def purchasePlan(request):
    plan_id = request.GET['plan_id']
    try:
        plan = Plan.objects.get(pk=plan_id)
    except Plan.DoesNotExist:
        messages.error(request, 'Invalid request. Please select the plan.')
        return redirect('plans')
    get_tax = TaxOnPlan.objects.all()
    tax_dict = {}
    for i in get_tax:
        tax_type = i.tax_type
        tax_value = i.tax_value
        tx_amount = round((float(tax_value) * plan.plan_price)/100, 2)
        tax_dict.update({tax_type: {float(tax_value):float(tx_amount)}})

    tax = sum(x for counter in tax_dict.values() for x in counter.values())
    grand_total = round(plan.plan_price + tax, 2)
    context = {
        'plan': plan,
        'tax_dict': tax_dict,
        'grand_total': grand_total,
        'tax': tax,
    }
    return render(request, 'business/purchasePlan.html', context)



def planPayment(request):
    body = json.loads(request.body)
    current_user = request.user
    business = Business.objects.get(user=current_user)
    order = PlanOrder.objects.get(business=business, ordered=False, order_number=body['orderID'])
    # Store transaction details inside payment model

    payment = PlanPayment(
        business = business,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount = body['total'],
        status = body['status'],
    )
    payment.save()

    # Update order model
    order.plan_payment = payment
    if body['status'] == 'COMPLETED':
        order.ordered = True
    else:
        messages.error(request, 'Payment failed. Please try again')
        return redirect('plans')
    order.save()

    # Upgrade plan
    # Get the current plan date
    current_exp_date = business.account_expiry_date
    # Get the purchased plan frequency
    purchased_plan = order.plan.plan_frequency
    if purchased_plan == 'monthly':
        plan_days = 30
    elif purchased_plan == 'quarterly':
        plan_days = 90
    elif purchased_plan == 'half-yearly':
        plan_days = 180
    elif purchased_plan == 'annually':
        plan_days = 365
    else:
        messages.error(request, 'Invalid plan. Please contact Altocan support.')
        return redirect('plans')
    exp_date = datetime.strptime(str(current_exp_date), '%Y-%m-%d')
    get_today = date.today()
    today = datetime.strptime(str(get_today), '%Y-%m-%d')
    if today > exp_date:
        end_date = today + timedelta(days=plan_days)
    else:
        end_date = exp_date + timedelta(days=plan_days)
    business.account_expiry_date = end_date
    business.save()
    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('business/plan_order_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def planOrder(request):
    current_user = request.user
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        tax = request.POST['tax']
        tax_data = request.POST['tax_data']
        total = request.POST['total']
        payment_method = request.POST['payment_method']
        plan_price = request.POST['plan_price']

        data = PlanOrder()
        data.business_id = current_user.id
        # data.plan_payment =
        data.plan_id = plan_id
        data.total = total
        data.tax = tax
        data.tax_data = tax_data
        data.ip = request.META.get('REMOTE_ADDR')

        # Calculate Account Manager's Commission
        business = Business.objects.get(user=current_user)
        account_manager = business.regional_manager
        try:
            get_account_manager = RegionalManager.objects.get(user=account_manager)
            commission_percent = get_account_manager.commission_percentage
        except RegionalManager.DoesNotExist:
            commission_percent = 0
        commission_amount = round((commission_percent * float(plan_price))/100, 2)
        data.account_manager_commission = commission_amount
        data.save()
        # Generate Plan Order Number
        if 'planOrder' in request.path:
            import datetime
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = 'P'+current_date + str(data.id)
        data.order_number = order_number
        data.save()
        request.session['plan_order_number'] = order_number
        business = Business.objects.get(user=current_user)
        try:
            plan_order = PlanOrder.objects.get(business=business, ordered=False, order_number=order_number)
        except PlanOrder.DoesNotExist:
            plan_order = None
    else:
        return redirect('plans')


    # Converting tax_data string to dict for better looping in the template
    tax_data = ast.literal_eval(tax_data)
    context = {
        'plan_order': plan_order,
        'tax': tax,
        'tax_data': tax_data,
        'total': total,
        'payment_method': payment_method,
    }
    return render(request, 'business/planPayment.html', context)



def plan_order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('payment_id')

    try:
        order = PlanOrder.objects.get(order_number=order_number)
        payment = PlanPayment.objects.get(payment_id=transaction_id)

        context = {
            'order': order,
            'payment': payment,
        }
        return render(request, 'business/plan_order_complete.html', context)
    except (PlanPayment.DoesNotExist, PlanOrder.DoesNotExist):
        return redirect('plans')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def planPurchaseHistory(request):
    plan_orders = PlanOrder.objects.filter(ordered=True).order_by('-created_at')
    business = Business.objects.get(user=request.user)
    account_expiry_date = business.account_expiry_date
    current_plan = Plan.objects.get(pk=business.plan_id)
    # Check if plan expired
    exp_date = datetime.strptime(str(account_expiry_date), '%Y-%m-%d')
    get_today = date.today()
    today = datetime.strptime(str(get_today), '%Y-%m-%d')
    if today < exp_date:
        is_expired = False
    else:
        is_expired = True
    context = {
        'plan_orders': plan_orders,
        'account_expiry_date': account_expiry_date,
        'current_plan': current_plan,
        'is_expired': is_expired,
    }
    return render(request, 'business/planPurchaseHistory.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def planHistoryDetail(request, pk=None):
    planHistoryDetail = get_object_or_404(PlanOrder, pk=pk)
    subtotal = planHistoryDetail.total - planHistoryDetail.tax
    context = {
        'planHistoryDetail': planHistoryDetail,
        'subtotal': subtotal,
    }
    return render(request, 'business/planHistoryDetail.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allCustomers(request):
    customers = Customer.objects.filter(user__is_customer=True).order_by('-created_date')
    paginator = Paginator(customers, 15)
    page = request.GET.get('page')
    paged_customers = paginator.get_page(page)
    context = {
        'customers': paged_customers,
    }
    return render(request, 'business/allCustomers.html', context)


def CustomerViewProfile(request, pk=None):
    try:
        customer = Customer.objects.get(user__id=pk, user__is_customer=True)
    except Customer.DoesNotExist:
        messages.error(request, 'Invalid request. Please try again')
        return redirect('allCustomers')

    context = {
        'customer': customer,
    }
    return render(request, 'business/CustomerViewProfile.html', context)


def setTax(request, pk=None):
    # try:
    #     tax = TaxSetting.objects.get(pk=pk)
    # except:
    #     tax = 0
    business = Business.objects.get(user=request.user)
    tax = get_object_or_404(TaxSetting, pk=pk)
    for i in tax:
        print(i)
    if request.method == 'POST':
        form = PaymentSettingForm(request.POST, instance=pay_setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your payment settings are saved successfully.')
            return redirect('/business/paymentSettings/'+str(pk))
    else:
        form = PaymentSettingForm(instance=pay_setting)

    context = {
        'form': form,
    }
    return render(request, 'business/setTax.html')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def setTax(request, business_id=None):
    tax = get_object_or_404(Tax, business_id=business_id)
    TaxSettingFormSet = inlineformset_factory(Tax, TaxSetting, form=TaxSettingForm, extra=1)

    if request.method == 'POST':
        add_another = request.POST['add_another']
        formset = TaxSettingFormSet(request.POST, instance=tax)
        if formset.is_valid():
            formset.save()
            tax.save()
            if add_another == 'true':
                return redirect('setTax', business_id)
            else:
                messages.success(request, 'Tax Added Successfully.')
                return redirect('setTax', business_id)
        else:
            return HttpResponse(formset.errors)
    else:
        formset = TaxSettingFormSet(instance=tax)

    context = {
        'tax' : tax,
        'formset': formset,
    }
    return render(request, 'business/setTax.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allInquiries(request):
    inquiries = Inquiry.objects.filter(business__user=request.user).order_by('-create_date')
    paginator = Paginator(inquiries, 15)
    page = request.GET.get('page')
    paged_inquiries = paginator.get_page(page)
    context = {
        'inquiries': paged_inquiries,
    }
    return render(request, 'business/allInquiries.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def viewInquiry(request, pk=None):
    try:
        inquiry = Inquiry.objects.get(pk=pk)
    except Inquiry.DoesNotExist:
        messages.error(request, 'Invalid request. Please try again')
        return redirect('allInquiries')
    context = {
        'inquiry': inquiry,
    }
    return render(request, 'business/viewInquiry.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteInquiry(request, pk=None):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.delete()
    messages.success(request, 'Inquiry has been deleted successfully.')
    return redirect('allInquiries')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allReviewRatings(request):
    reviewratings = ReviewRating.objects.all().order_by('-create_at')
    paginator = Paginator(reviewratings, 15)
    page = request.GET.get('page')
    paged_reviewratings = paginator.get_page(page)
    context = {
        'reviewratings': paged_reviewratings,
    }
    return render(request, 'business/allReviewRatings.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def toggleApproval(request, pk=None):
    event = request.GET.get('event')
    reviewrating = get_object_or_404(ReviewRating, pk=pk)
    reviewrating.status = event.capitalize()
    reviewrating.save()

    reviewrating = get_object_or_404(ReviewRating, pk=pk)
    if reviewrating.status:
        return HttpResponse('true')
    else:
        return HttpResponse('false')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allColors(request):
    colors = Color.objects.all()
    paginator = Paginator(colors, 25)
    page = request.GET.get('page')
    paged_colors = paginator.get_page(page)
    context = {
        'colors': paged_colors,
    }
    return render(request, 'business/allColors.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allSizes(request):
    sizes = Size.objects.all()
    paginator = Paginator(sizes, 25)
    page = request.GET.get('page')
    paged_sizes = paginator.get_page(page)
    context = {
        'sizes': paged_sizes,
    }
    return render(request, 'business/allSizes.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addColor(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Color Added Successfully')
            return redirect('allColors')
        else:
            print(form.errors)

    form = ColorForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addColor.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addSize(request):
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Size Added Successfully')
            return redirect('allSizes')
        else:
            print(form.errors)

    form = SizeForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addSize.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editColor(request, pk=None):
    color = get_object_or_404(Color, pk=pk)
    if request.method == 'POST':
        form = ColorForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            messages.success(request, 'Color Added Successfully')
            return redirect('allColors')
        else:
            print(form.errors)

    form = ColorForm(instance=color)
    context = {
        'form': form,
        'color': color,
    }
    return render(request, 'business/editColor.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editSize(request, pk=None):
    size = get_object_or_404(Size, pk=pk)
    if request.method == 'POST':
        form = SizeForm(request.POST, instance=size)
        if form.is_valid():
            form.save()
            messages.success(request, 'Size Added Successfully')
            return redirect('allSizes')
        else:
            print(form.errors)

    form = SizeForm(instance=size)
    context = {
        'form': form,
        'size': size,
    }
    return render(request, 'business/editSize.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteColor(request, pk=None):
    color = get_object_or_404(Color, pk=pk)
    color.delete()
    messages.success(request, 'Color has been deleted.')
    return redirect('allColors')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteSize(request, pk=None):
    size = get_object_or_404(Size, pk=pk)
    size.delete()
    messages.success(request, 'Size has been deleted.')
    return redirect('allSizes')


#blogs
#allBlogs
login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allBlogs(request):
    business = get_object_or_404(Business, pk=request.user.id)
    blogs= Blog.objects.filter(business=business).order_by('-created_on')
    paginator = Paginator(blogs, 15)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)

    # get blog activation status
    blog_activation = BlogActivation.objects.get(business=business)

    context = {
        'blogs': paged_blogs,
        'blog_activation': blog_activation,
    }
    return render(request, 'business/allBlogs.html', context)

#addBlog
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addBlog(request):
    if request.method == 'POST':
        blogInfo_form = BlogForm(request.POST, request.FILES)
        if blogInfo_form.is_valid():
            current_user = request.user
            business_name = Business.objects.get(user=current_user)
            title  = blogInfo_form.cleaned_data['title']
            blog  = blogInfo_form.save(commit=False)
            blog.business = business_name
            blog.slug = slugify(title)
            blog.author = current_user.name
            blogInfo_form.save()
            messages.success(request, 'You have added a new blog!')
            return redirect('allBlogs')
        else:
            print(blogInfo_form.errors)
            messages.error(request, 'Something went wrong!')
            return redirect('allBlogs')
    else:
        blogInfo_form = BlogForm()
    context = {
        'blogInfo_form': blogInfo_form,
    }
    return render(request, 'business/addBlog.html', context)

#deleteBlog
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteBlog(request, pk=None):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    messages.success(request, 'Blog has been deleted.')
    return redirect('allBlogs')

#editBlog
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editBlog(request, pk=None):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blogInfo_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blogInfo_form.is_valid():
            blogInfo_form.save()
            messages.success(request, 'Blog has been updated.')
            return redirect('allBlogs')
        else:
            messages.error(request, 'Something went wrong, please try again!')
            return redirect('allBlogs')
    else:
        blogInfo_form = BlogForm(instance=blog)
    context = {
        'blogInfo_form': blogInfo_form,
        'blog': blog,
    }
    return render(request, 'business/editBlog.html', context)

#blogCategories
#allBlogsCategories
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allBlogsCategories(request):
    blogcategories = BlogCategory.objects.all()
    context = {
        'blogcategories': blogcategories,
    }
    return render(request, 'business/allBlogsCategories.html', context)

#addBlogCategory
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addBlogCategories(request):
    if request.method == 'POST':
        blogform = BlogCategoryForm(request.POST, request.FILES)
        if blogform.is_valid():
            category_name = blogform.cleaned_data['category_name']
            blogcategory = blogform.save(commit=False)
            blogcategory.slug = slugify(category_name)
            blogform.save()
            messages.success(request, 'Category Added Successfully')
            return redirect('allBlogsCategories')
        else:
            print(blogform.errors)

    blogform = BlogCategoryForm()
    context = {
        'blogform': blogform,
    }
    return render(request, 'business/addBlogCategory.html', context)

#deleteBlogCategory
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteBlogCategory(request, pk=None):
    category = get_object_or_404(BlogCategory, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted.')
    return redirect('allBlogsCategories')

#editBlogCategory

@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editBlogCategory(request, pk=None):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Modified Successfully')
            return redirect('allBlogsCategories')
        else:
            print(form.errors)

    else:
        form = BlogCategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'business/editBlogCategory.html', context)


#blog_comments
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allComments(request):
    comments = Comment.objects.filter(reply=None).order_by('-created_on').annotate(number_of_replies=Count('replies')) # annotate the queryset
    paginator = Paginator(comments, 15)
    page = request.GET.get('page')
    paged_comments = paginator.get_page(page)
    context = {
        'comments': paged_comments,
    }
    return render(request, 'business/allComments.html', context)

#commentsapproval
@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def commentApproval(request, pk=None):
    event = request.GET.get('event')
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_active = event.capitalize()
    comment.save()

    comment = get_object_or_404(Comment, pk=pk)
    if comment.is_active:
        return HttpResponse('true')
    else:
        return HttpResponse('false')

@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def commentReplies(request, pk=None):
    single_comment = Comment.objects.get(pk=pk)
    replies = single_comment.replies.order_by('-created_on')
    paginator = Paginator(replies, 15)
    page = request.GET.get('page')
    paged_replies = paginator.get_page(page)
    context = {
        'replies': paged_replies,
        'single_comment': single_comment,
    }
    return render(request, 'business/commentReplies.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allContacts(request):
    contacts = SiteContact.objects.filter(business__user=request.user).order_by('-create_date')
    paginator = Paginator(contacts, 15)
    page = request.GET.get('page')
    paged_contacts = paginator.get_page(page)
    context = {
        'contacts': paged_contacts,
    }
    return render(request, 'business/allContacts.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def viewContact(request, pk=None):
    try:
        contact = SiteContact.objects.get(pk=pk)
    except SiteContact.DoesNotExist:
        messages.error(request, 'Invalid request. Please try again')
        return redirect('allContacts')
    context = {
        'contact': contact,
    }
    return render(request, 'business/viewContact.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteContact(request, pk=None):
    contact = get_object_or_404(SiteContact, pk=pk)
    contact.delete()
    messages.success(request, 'Contact request has been deleted successfully.')
    return redirect('allContacts')


def blogEnableToggle(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    blog_activation = get_object_or_404(BlogActivation, business=business)
    if event == 'true':
        blog_activation.is_enabled = True
        blog_activation.save()
        result = 'enabled'
    else:
        blog_activation.is_enabled = False
        blog_activation.save()
        result = 'disabled'
    return HttpResponse(result)


def productEnableToggle(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    product_activation = get_object_or_404(ProductActivation, business=business)
    if event == 'true':
        product_activation.is_enabled = True
        product_activation.save()
        result = 'enabled'
    else:
        product_activation.is_enabled = False
        product_activation.save()
        result = 'disabled'
    return HttpResponse(result)



@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allServices(request):
    # business = get_object_or_404(Business, pk=request.user.id)
    services = Service.objects.filter(business=request.user.id).order_by('-created_date')

    # get service activation status
    service_activation = ServiceActivation.objects.get(business=request.user.id)
    context = {
        'services': services,
        'service_activation': service_activation,
    }
    return render(request, 'business/allServices.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editService(request, pk=None):
    url = request.META.get('HTTP_REFERER')
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service has been updated.')
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Invalid form, please try again.')
            return HttpResponseRedirect(url)

    else:
        form = ServiceForm(instance=service)
    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'business/editService.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addService(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            business = Business.objects.get(user=request.user)
            # product_name = basicInfo_form.cleaned_data['product_name']
            service = form.save(commit=False)
            service.business = business
            service.save()
            messages.success(request, 'New service has been created.')
            return redirect('allServices')
        else:
            messages.error(request, 'Invalid form, please try again.')
            return redirect('addService')
    else:
        form = ServiceForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addService.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteService(request, pk=None):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, 'Service has been deleted.')
    return redirect('allServices')


def serviceEnableToggle(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    service_activation = get_object_or_404(ServiceActivation, business=business)
    if event == 'true':
        service_activation.is_enabled = True
        service_activation.save()
        result = 'enabled'
    else:
        service_activation.is_enabled = False
        service_activation.save()
        result = 'disabled'
    return HttpResponse(result)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def allPortfolio(request):
    portfolio = Portfolio.objects.filter(business=request.user.id).order_by('-created_date')

    # get service activation status
    portfolio_activation = PortfolioActivation.objects.get(business=request.user.id)
    context = {
        'portfolio': portfolio,
        'portfolio_activation': portfolio_activation,
    }
    return render(request, 'business/allPortfolio.html', context)


def portfolioEnableToggle(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    portfolio_activation = get_object_or_404(PortfolioActivation, business=business)
    if event == 'true':
        portfolio_activation.is_enabled = True
        portfolio_activation.save()
        result = 'enabled'
    else:
        portfolio_activation.is_enabled = False
        portfolio_activation.save()
        result = 'disabled'
    return HttpResponse(result)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editPortfolio(request, pk=None):
    url = request.META.get('HTTP_REFERER')
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('/business/editPortfolio/'+str(pk)+'/editPortfolioGallery/')
        else:
            messages.error(request, 'Invalid form, please try again.')
            return HttpResponseRedirect(url)

    else:
        form = PortfolioForm(instance=portfolio)
    context = {
        'form': form,
        'portfolio': portfolio,
    }
    return render(request, 'business/editPortfolio.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addPortfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            business = Business.objects.get(user=request.user)
            portfolio = form.save(commit=False)
            portfolio.business = business
            portfolio.save()
            pk = portfolio.id
            makeSlug = portfolio.title + str(pk)
            portfolio.slug = slugify(makeSlug)
            portfolio.save()
            messages.success(request, 'New item has been added to your portfolio.')
            return redirect('/business/editPortfolio/'+str(pk)+'/editPortfolioGallery/')
        else:
            messages.error(request, 'Invalid form, please try again.')
            return redirect('addPortfolio')
    else:
        form = PortfolioForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addPortfolio.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deletePortfolio(request, pk=None):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    portfolio.delete()
    messages.success(request, 'Portfolio item has been deleted.')
    return redirect('allPortfolio')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editPortfolioGallery(request, pk=None):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    PortfolioGalleryFormSet = inlineformset_factory(Portfolio, PortfolioGallery, form=PortfolioGalleryForm, extra=1)

    if request.method == 'POST':
        add_another = request.POST['add_another']
        formset = PortfolioGalleryFormSet(request.POST, request.FILES, instance=portfolio)
        if formset.is_valid():
            formset.save()
            if add_another == 'true':
                return redirect('/business/editPortfolio/'+str(pk)+'/editPortfolioGallery/')
            elif add_another == 'finish':
                portfolio.is_active = True
                portfolio.save()
                messages.success(request, 'Portfolio has been uploaded successfully.')
                return redirect('allPortfolio')
            else:
                return redirect('/business/editPortfolio/'+str(pk)+'/editPortfolioGallery/')
        else:
            return HttpResponse(formset.errors)
    else:
        formset = PortfolioGalleryFormSet(instance=portfolio)
    
    context = {
        'portfolio' : portfolio,
        'formset': formset,
    }
    return render(request, 'business/editPortfolioGallery.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def customVariants(request):
    product_attr = ProductAttribute.objects.all()
    attr_values = AttributeValue.objects.all()
    context = {
        'product_attr': product_attr,
        'attr_values': attr_values,
    }
    return render(request, 'business/customVariants.html', context)


def addVariant(request):
    if request.method == 'POST':
        form = ProductAttributeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variant Added Successfully')
            return redirect('customVariants')
        else:
            print(form.errors)

    form = ProductAttributeForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addVariant.html', context)


def editVariant(request, pk=None):
    pro_attribute = get_object_or_404(ProductAttribute, pk=pk)
    if request.method == 'POST':
        form = ProductAttributeForm(request.POST, instance=pro_attribute)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variant Updated Successfully')
            return redirect('customVariants')
        else:
            print(form.errors)

    form = ProductAttributeForm(instance=pro_attribute)
    context = {
        'form': form,
    }
    return render(request, 'business/editVariant.html', context)


def deleteVariant(request, pk=None):
    pro_attribute = get_object_or_404(ProductAttribute, pk=pk)
    pro_attribute.delete()
    messages.success(request, 'Product Variant has been deleted.')
    return redirect('customVariants')


def addVariantValue(request):
    if request.method == 'POST':
        form = AttributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Variant value has been assigned.')
            return redirect('customVariants')
        else:
            print(form.errors)

    form = AttributeValueForm()
    context = {
        'form': form,
    }
    return render(request, 'business/addVariantValue.html', context)


def editVariantValue(request, pk=None):
    attribute_value = get_object_or_404(AttributeValue, pk=pk)
    if request.method == 'POST':
        form = AttributeValueForm(request.POST, instance=attribute_value)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attribute Value Updated Successfully')
            return redirect('customVariants')
        else:
            print(form.errors)

    form = AttributeValueForm(instance=attribute_value)
    context = {
        'form': form,
    }
    return render(request, 'business/editVariantValue.html', context)


def deleteVariantValue(request, pk=None):
    attribute_value = get_object_or_404(AttributeValue, pk=pk)
    attribute_value.delete()
    messages.success(request, 'Variant value has been deleted.')
    return redirect('customVariants')