from emails.models import BusinessEmailSetting
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from accounts.models import Business
from .models import Inquiry
from django.core.mail import get_connection, send_mail
from datetime import datetime
import time
from datetime import timedelta

from .models import SiteContact
import random
from django.http import HttpResponse
from django.core.mail import EmailMessage





def inquiry(request):
    if request.method == 'POST':
        business_id = request.POST['business_id']
        user_id = request.POST['user_id']
        product_id = request.POST['product_id']
        product_name = request.POST['product_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        inq_message = request.POST['inq_message']

        business = Business.objects.get(business_id=business_id)


        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Inquiry.objects.all().filter(product_id=product_id, user_id=user_id)
            if has_contacted:
                return HttpResponse('already-inquired')

        inquiry = Inquiry(business=business, user_id=user_id, product_id=product_id,
        product_name=product_name, first_name=first_name, last_name=last_name, email=email,
        phone=phone, inq_message=inq_message)

        business_email = business.user.email
        mail_subject = 'New Product Inquiry'
        message = render_to_string('pages/product_inquiry_email.html', {
                        'inquiry': inquiry,
                        'product_name': product_name,
                    })
        to_email = business_email
        # Get Email Connection
        email_settings = BusinessEmailSetting.objects.get(business=business)
        from_email = email_settings.email_host_user
        with get_connection(
            host=email_settings.email_host,
            port=email_settings.port,
            username=email_settings.email_host_user,
            password=email_settings.email_host_password,
            use_tls=email_settings.email_use_tls
        ) as connection:
            email_send = EmailMessage(mail_subject, message, from_email, to=[to_email],
                            connection=connection)
        email_send.send()
        inquiry.save()
        return HttpResponse('Your inquiry has been submitted. Our representative will get in touch with you soon.')
    else:
        return HttpResponse('GET method not allowed')




def contact(request):
    if request.method == 'POST':
        business_id = request.POST['business_id']
        user_id = request.POST['user_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        contact_message = request.POST['contact_message']

        business = Business.objects.get(business_id=business_id)
        contact = SiteContact(business=business, user_id=user_id, name=name, email=email,
        phone=phone, subject=subject, contact_message=contact_message)
        contact.save()
        mail_subject = 'You have a new message from the website contact form'
        message = render_to_string('pages/contact_form_email.html', {
            'contact': contact,
        })
        to_email = business.user.email
        email_send = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email_send.send()
        messages.success(request, 'Your message has been submitted. We will get back to you soon.')
        return redirect('contact_page')
    else:
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('contact_page')


def verify_otp(request):
    email = request.session['email']
    id = request.session['id']
    business_email = request.session['business_email']
    if request.method == 'POST':
        otp = request.POST.get('otp')
        contact = SiteContact.objects.get(email=email, id=id)
        # get otp updated time
        get_updated_time = contact.otp_updated_time
        datetime_get_updated_time = datetime.strptime(get_updated_time, '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.now()
        difference = (current_time - datetime_get_updated_time).total_seconds() # convert difference time to seconds
        if difference >= 90:
            contact.is_otp_expired = True
            contact.save()
            return HttpResponse('Invalid OTP')
        else:
            if contact.otp == otp:
                mail_subject = 'You have a new message from the website contact form'
                message = render_to_string('pages/contact_form_email.html', {
                    'contact': contact,
                })
            
                to_email = business_email
                email_send = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email_send.send()
                contact.is_otp_verified = True
                contact.save()
                return HttpResponse('verified')
            else:
                return HttpResponse('wrong-otp')


def resend_otp(request):
    email = request.session['email']
    id = request.session['id']
    business_email = request.session['business_email']
    contact = SiteContact.objects.get(email=email, id=id)
    if contact.is_otp_verified:
        return HttpResponse('Your OTP is already verified')
    else:
        try:
            otp = str(random.randint(100000,999999))
            contact = SiteContact.objects.get(email=email, id=id)
            contact.otp = otp
            contact.save()
            if contact.otp_resend_counter >= 3:
                return HttpResponse('You have exceeded the maximum attempts of resending OTP. Please try different email address.')
            else:
                business_name = contact.business
                mail_subject = 'Your One Time Password is here'
                message = render_to_string('pages/contact_form_otp_email.html', {
                    'business_name': business_name,
                    'name': contact.name,
                    'otp': otp,
                })
            
                to_email = email
                email_send = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email_send.send()
                contact.otp_resend_counter += 1
                contact.save()
                return HttpResponse('otp sent')
        except:
            pass
