from products.views import is_productSelling_activated
from sitesettings.models import CashOnDelivery, DirectDepositEmail, PaypalConfig
from orders.models import Payment
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from category.models import Category
from .models import Tax, ShopCart, ShopCartForm, TaxSetting
from accounts.models import Business, Country
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlparse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from orders.forms import BillingUserInfoForm, BillingCustomerInfoForm

# Get the cart_id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Add to cart method
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')


# AJAX
def add_cart_ajax(request, product_id):
    product_id = request.POST['product_id']
    quantity = request.POST['quantity']
    return product_id





# Remove cart item
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')





# Delete the whole cart item
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


# Cart method
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        biz_id = Business.objects.get(user__is_business=True, is_account_verified=True)
        get_tax = Tax.objects.get(business__business_id=biz_id.business_id)
        tax_percent = get_tax.tax_percentage
        tax = round((tax_percent * total)/100, 2)
        grand_total = round(total + tax, 2)
    except ObjectDoesNotExist:
        pass # ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'tax_percent' : tax_percent,
        'grand_total': grand_total,
    }
    return render(request, 'shop/cart.html', context)


@login_required(login_url='/userLogin')
def addtoshopcart(request,product_id):
    id = product_id
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    
    product= Product.objects.get(pk=id)
    if product.variant != 'None':
        if product.variant  == 'Custom':
            variantid = request.POST.get('customVariantId')
        else:
            variantid = request.POST.get('variantid')  # from variant add to cart
        
        print('variantid', variantid)
        
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        # Construct message
        command = request.POST['command']
        if command == 'add':
            message = 'Product has been added to the cart.'
        elif command == 'update':
            message = ''
        else:
            message = 'Product updated.'

        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                if product.variant != 'None':
                    data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, message)
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Insert to Shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


@login_required(login_url='/userLogin')
def delete_itemfromcart(request, product_id):
    id = product_id
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)
    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        # Construct message
        command = request.POST['command']
        if command == 'add':
            message = 'Product has been added to the cart.'
        elif command == 'update':
            message = ''
        else:
            message = 'Product updated.'

        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                if data.quantity > 1:
                    data.quantity -= form.cleaned_data['quantity']
                    data.save()  # save data
                else:
                    data.delete()
        return HttpResponseRedirect(url)



@is_productSelling_activated
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id).order_by('created_at')

    total=0
    # tax = 0
    # grand_total = 0
    # tax_percent = 0
    for i in shopcart:
        if i.product.variant != 'None':
            total += i.variant.price * i.quantity
        else:
            total += i.product.price * i.quantity

    # url = request.build_absolute_uri()
    # domain = urlparse(url).netloc
    # biz_id = Business.objects.get(domain_name=domain)
    # get_tax = TaxSetting.objects.all()
    # tax_dict = {}
    # for i in get_tax:
    #     tax_type = i.tax_type
    #     tax_value = i.tax_value
    #     tx_amount = round((tax_value * total)/100, 2)
    #     tax_dict.update({tax_type: {tax_value:tx_amount}})

    # tax = sum(x for counter in tax_dict.values() for x in counter.values())
    # grand_total = round(total + tax, 2)

    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             # 'tax_percent': tax_percent,
             # 'tax': tax,
             # 'grand_total': grand_total,
             }
    return render(request,'shop/cart.html', context)


def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Item has been removed form the Cart.")
    return HttpResponseRedirect("/shopcart")


@is_productSelling_activated
def checkout(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    cart_count = shopcart.count()
    if cart_count <= 0:
        return redirect('shop')
    else:
        userinfo_form = BillingUserInfoForm(instance=current_user)
        customerinfo_form = BillingCustomerInfoForm()
        
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        dd = DirectDepositEmail.objects.get(business=business)
        pp = PaypalConfig.objects.get(business=business)
        cod = CashOnDelivery.objects.get(business=business)
        context = {
            'userinfo_form': userinfo_form,
            'customerinfo_form': customerinfo_form,
            'dd': dd,
            'pp': pp,
            'cod': cod,
        }
        return render(request, 'shop/checkout.html', context)
