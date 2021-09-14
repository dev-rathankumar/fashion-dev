from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NewsletterUser
from .forms import EmailSubscribeForm
from django.contrib import messages

from django.conf import settings
import json
import requests


MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0/'


members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'

def subscribe(email):
    data = {
        'email_address': email,
        'status': 'subscribed',
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data),
    )
    return r.status_code, r.json()


def email_list_subscribe(request):
    form = EmailSubscribeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_queryset = NewsletterUser.objects.filter(email=form.instance.email)
            if email_signup_queryset.exists():
                # messages.info(request, "You are already subscribed!")
                return HttpResponse("You are already subscribed!")
            else:
                subscribe(form.instance.email)
                form.save()
                # messages.success(request, "Thank you for subscribing to our newsletters!")
                return HttpResponse("Thank you for subscribing to our newsletters!")
        else:
            print(form.errors)
            return HttpResponse('Something went wrong. Please try again!')
    return redirect(request.META.get("HTTP_REFERER"))
