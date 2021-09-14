from django.template.defaultfilters import lower
from orders.forms import DDPaymentForm
from sitesettings.models import CashOnDelivery, DirectDepositEmail, Footer, Header
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from carts.models import ShopCart, Tax, TaxSetting
from products.models import Product, Variants
from .models import OrderForm, Order, OrderProduct, Payment, StoreLocation
from django.utils.crypto import get_random_string
from django.contrib import messages
from accounts.models import Business
from urllib.parse import urlparse
import datetime
from django.core.mail import send_mail
import json
from django.core import serializers
from django.conf import settings
from decimal import Decimal
from random import randint


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, ordered=False, order_number=body['orderID'])

    # Create and save payment instance
    payment = Payment(
        user = request.user,
        payment_id = body['payID'],
        payment_method = body['paymentMethod'],
        amount = order.total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.ordered = True
    order.save()

    # Move cart items to Order Products table
    shopcart = ShopCart.objects.filter(user_id=request.user.id)
    for item in shopcart:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id # Order Id
        orderproduct.payment = payment
        orderproduct.product_id = item.product_id
        if item.product.variant != 'None':
            orderproduct.variant_id = item.variant.id
            orderproduct.color = item.color
            orderproduct.size = item.size
            orderproduct.price = item.variant.price
        else:
            orderproduct.price = item.product.price
        orderproduct.user_id = request.user.id
        orderproduct.quantity = item.quantity
        orderproduct.amount = item.amount
        orderproduct.status = "New"
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce quantity of sold products from the product db
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        variants = Variants.objects.filter(id=item.variant_id)
        for var in variants:
            var.quantity -= item.quantity
            var.save()

    ordered_products = OrderProduct.objects.filter(order_id=orderproduct.order_id)
    order = Order.objects.get(order_number=order.order_number)
    subtotal = 0
    for i in ordered_products:
        if i.product.variant == 'None':
            subtotal += i.product.price * i.quantity
        else:
            subtotal += i.variant.price * i.quantity

    ShopCart.objects.filter(user_id=request.user.id).delete() # Clear & Delete shopcart
    request.session['cart_items'] = 0

    current_site = get_current_site(request)
    business = Business.objects.get(domain_name=current_site.domain)
    header = Header.objects.get(business=business)
    footer = Footer.objects.get(business=business)
    support_email = business.user.email
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_placed_email.html', {
        'order': order,
        'business': business,
        'header': header,
        'footer': footer,
        'support_email': support_email,
        'ordered_products': ordered_products,
        'domain': current_site.domain,
        'subtotal': subtotal,
        'payment': payment,
    })
    to_email = order.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()

    context = {
        'order_number': order.order_number,
        'ordered_products': ordered_products,
        'order': order,
        'subtotal': subtotal,
        'payment': payment,
    }
    data = {
        'order_number': order.order_number,
        'payment_id': payment.payment_id,
    }
    return JsonResponse(data)


def orderproduct(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    cart_count = shopcart.count()
    if cart_count <= 0:
        return redirect('shop')
    # Calculate Grand Total
    # total=0
    # tax = 0
    # grand_total = 0
    # tax_percent = 0
    # for i in shopcart:
    #     total += i.variant.price * i.quantity

    
    biz_id = Business.objects.get(user__is_business=True, is_account_verified=True)
    # grand_total = request.session.get('grand_total')
    # print(grand_total)
    # tax = request.session['tx_amount']

    # grand_total = Decimal(grand_total)
    # tax = Decimal(tax)

    # get_tax = TaxSetting.objects.all()
    # tax_dict = {}
    # for i in get_tax:
    #     tax_type = i.tax_type
    #     tax_value = i.tax_value
    #     tx_amount = round((tax_value * total)/100, 2)
    #     tax_dict.update({tax_type: {float(tax_value):float(tx_amount)}})

    # tax = sum(x for counter in tax_dict.values() for x in counter.values())
    # grand_total = round(float(total) + tax, 2)

    if request.method == 'POST':
        grand_total = request.POST['grand_total']
        tax = request.POST['tax']
        form = OrderForm(request.POST)
        phone = request.POST['phone_number']
        payment_method = request.POST['payment_method']
        
        if form.is_valid():
            # Send credit card info to bank and get the result.
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = phone
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin_code = form.cleaned_data['pin_code']
            data.payment_method = payment_method
            if payment_method == 'Direct Deposit' or payment_method == 'Cash On Delivery':
                data.status = 'On Hold'
            data.note = form.cleaned_data['note']
            data.user_id = current_user.id
            data.total = grand_total
            # data.tax_data = tax_dict
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            request.session['order_number'] = order_number
            request.session['payment_method'] = payment_method
            order = Order.objects.get(user=current_user, ordered=False, order_number=order_number)

            # render dd form
            dd_paymentForm = DDPaymentForm()
            # get direct deposit email address
            ddEmail = ''
            if payment_method == 'Direct Deposit':
                dd = DirectDepositEmail.objects.get(business=biz_id)
                ddEmail = dd.direct_deposit_email
            elif payment_method == 'Cash On Delivery':
                cod = CashOnDelivery.objects.get(business=biz_id)
                codStatus = cod.is_enabled
                store_locations = StoreLocation.objects.all()
                location_count = store_locations.count()
            else:
                ddEmail = ''
            context = {
                'order' : order,
                'payment_method': payment_method,
                'dd_paymentForm': dd_paymentForm,
                'ddEmail': ddEmail,
                'codStatus': codStatus,
                'store_locations': store_locations,
                'location_count': location_count,
            }
            return render(request, 'orders/payments.html', context)
        else:
            print(form.errors)
            return redirect('checkout')
    else:
        return redirect('checkout')



def saveDDPayment(request):
    order_num = request.session.get('order_number')
    order = Order.objects.get(user=request.user, ordered=False, order_number=order_num)
    if request.method == 'POST':
        transDDForm = DDPaymentForm(request.POST, request.FILES)
        if transDDForm.is_valid:
            transDD = transDDForm.save(commit=False)
            user_id = request.user.id
            transDD.user_id = user_id
            transDD.payment_method = lower(order.payment_method)
            transDD.status = 'PENDING'
            transDD.save()
            payment = Payment.objects.get(id=transDD.id)

            order.payment = payment
            order.ordered = True
            order.save()

            # Move cart items to Order Products table
            shopcart = ShopCart.objects.filter(user_id=request.user.id)
            for item in shopcart:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id # Order Id
                orderproduct.payment = order.payment
                orderproduct.product_id = item.product_id
                if item.product.variant != 'None':
                    orderproduct.variant_id = item.variant.id
                    orderproduct.color = item.color
                    orderproduct.size = item.size
                    orderproduct.price = item.variant.price
                else:
                    orderproduct.price = item.product.price
                orderproduct.user_id = request.user.id
                orderproduct.quantity = item.quantity
                orderproduct.amount = item.amount
                orderproduct.status = "On Hold"
                orderproduct.ordered = True
                orderproduct.save()

                # Reduce quantity of sold products from the product db
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
                variants = Variants.objects.filter(id=item.variant_id)
                for var in variants:
                    var.quantity -= item.quantity
                    var.save()

            ordered_products = OrderProduct.objects.filter(order_id=orderproduct.order_id)
            order = Order.objects.get(order_number=order.order_number)
            subtotal = 0
            for i in ordered_products:
                if i.product.variant == 'None':
                    subtotal += i.product.price * i.quantity
                else:
                    subtotal += i.variant.price * i.quantity

            ShopCart.objects.filter(user_id=request.user.id).delete() # Clear & Delete shopcart
            request.session['cart_items'] = 0

            current_site = get_current_site(request)
            business = Business.objects.get(domain_name=current_site.domain)
            header = Header.objects.get(business=business)
            footer = Footer.objects.get(business=business)
            support_email = business.user.email
            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_placed_email.html', {
                'order': order,
                'business': business,
                'header': header,
                'footer': footer,
                'support_email': support_email,
                'ordered_products': ordered_products,
                'domain': current_site.domain,
                'subtotal': subtotal,
                'payment': payment,
                'direct_deposit': True,
            })
            to_email = order.user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()

            return redirect('/order/order_complete?order_number='+order.order_number+'&payment_id='+payment.payment_id)


def codPlaceOrder(request):
    order_num = request.session.get('order_number')
    order = Order.objects.get(user=request.user, ordered=False, order_number=order_num)
    if request.method == 'POST':
        location = request.POST['store_location']
        rand_no = randint(1000, 9999)
        cod_number = 'COD'+str(rand_no)+str(order.id)
        # Create and save payment instance
        payment = Payment(
            user = request.user,
            payment_id = cod_number,
            payment_method = lower(order.payment_method),
            amount = order.total,
            status = 'PENDING',
        )
        payment.save()
        order.payment = payment
        order.store_location_id = location
        order.ordered = True
        order.save()

        # Move cart items to Order Products table
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for item in shopcart:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id # Order Id
            orderproduct.payment = order.payment
            orderproduct.product_id = item.product_id
            if item.product.variant != 'None':
                orderproduct.variant_id = item.variant.id
                orderproduct.color = item.color
                orderproduct.size = item.size
                orderproduct.price = item.variant.price
            else:
                orderproduct.price = item.product.price
            orderproduct.user_id = request.user.id
            orderproduct.quantity = item.quantity
            orderproduct.amount = item.amount
            orderproduct.status = "On Hold"
            orderproduct.ordered = True
            orderproduct.save()

            # Reduce quantity of sold products from the product db
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
            variants = Variants.objects.filter(id=item.variant_id)
            for var in variants:
                var.quantity -= item.quantity
                var.save()

        ordered_products = OrderProduct.objects.filter(order_id=orderproduct.order_id)
        order = Order.objects.get(order_number=order.order_number)
        subtotal = 0
        for i in ordered_products:
            if i.product.variant == 'None':
                subtotal += i.product.price * i.quantity
            else:
                subtotal += i.variant.price * i.quantity

        ShopCart.objects.filter(user_id=request.user.id).delete() # Clear & Delete shopcart
        request.session['cart_items'] = 0

        current_site = get_current_site(request)
        business = Business.objects.get(domain_name=current_site.domain)
        header = Header.objects.get(business=business)
        footer = Footer.objects.get(business=business)
        support_email = business.user.email
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_placed_email.html', {
            'order': order,
            'business': business,
            'header': header,
            'footer': footer,
            'support_email': support_email,
            'ordered_products': ordered_products,
            'domain': current_site.domain,
            'subtotal': subtotal,
            'direct_deposit': True,
        })
        to_email = order.user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return redirect('/order/order_complete?order_number='+order.order_number+'&payment_id='+payment.payment_id)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            if i.product.variant == 'None':
                    subtotal += i.product.price * i.quantity
            else:
                subtotal += i.variant.price * i.quantity
        payment = Payment.objects.get(payment_id=transaction_id, pk=order.payment.id)
        context = {
            'order_number': order.order_number,
            'ordered_products': ordered_products,
            'order': order,
            'subtotal': subtotal,
            'transaction_id': payment.payment_id,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
