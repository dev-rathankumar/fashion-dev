from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from smart_selects.db_fields import ChainedForeignKey
import random
from django_dnf.fields import DomainNameField

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from datetime import datetime
from django.contrib.sites.models import Site

# Image manipulation
from io import BytesIO
from PIL import Image
from django.core.files import File
from plans.models import Plan

# Custom user model
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        # Add country for the first time creation of superadmin
        usr = User.objects.all().count()
        if usr >= 1:
            pass
        else:
            country = Country()
            country.country_name = 'Canada'
            country.save()
            state_list = [
                'Alberta (AB)',
                'British Columbia (BC)',
                'Manitoba (MB)',
                'New Brunswick (NB)',
                'Newfoundland and Labrador (NL)',
                'Northwest Territories (NT)',
                'Nova Scotia (NS)',
                'Nunavut (NU)',
                'Ontario (ON)',
                'Prince Edward Island (PE)',
                'Quebec (QC)',
                'Saskatchewan (SK)',
                'Yukon (YT)',
                ]
            for s in state_list:
                state = State()
                state.state_name = s
                state.country_id = 1
                state.save()
        return user


# Image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image

GenderChoice = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others')
)
# User model
class User(AbstractBaseUser):
    is_customer     = models.BooleanField(default=False)
    is_business     = models.BooleanField(default=False)
    is_regional_manager     = models.BooleanField(default=False)

    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    gender          = models.CharField(choices=GenderChoice, blank=True, max_length=50)
    profile_picture = models.ImageField(upload_to='accounts/%Y/%m/%d', default='default/default-user.png', blank=True)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @property
    def customer_id(self):
        if self.is_customer:
            cust = Customer.objects.get(pk=self.id)
            return cust.customer_id
        elif self.is_business:
            cust = Business.objects.get(pk=self.id)
            return cust.business_id
        elif self.is_regional_manager:
            cust = RegionalManager.objects.get(pk=self.id)
            return cust.regional_manager_id


    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'



class Country(models.Model):
    country_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.country_name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=255)

    def __str__(self):
        return self.state_name

# def upload_to(instance, filename):
#     return 'managers/%s/images/%s' % (instance.user.username, filename)

class RegionalManager(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    regional_manager_id     = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = ChainedForeignKey(
            State,
            chained_field="country",
            chained_model_field="country",
            show_all=False,
            auto_choose=True,
            sort=True
        )
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    date_of_joining = models.DateField()
    account_expiry_date = models.DateField()
    commission_percentage = models.FloatField(default=0)
    is_editing = models.BooleanField(default=False, blank=True, editable=False)
    is_verification_email_sent = models.BooleanField(default=False, editable=False)
    is_account_verified = models.BooleanField(default=False, editable=False)

    # Override save method
    def save(self, *args, **kwargs):
        if self.is_editing == False and self.is_verification_email_sent == False:
            # Send password reset and activation email
            current_site = Site.objects.get_current()
            mail_subject = 'Reset your password and activate your account.'
            message = render_to_string('accounts/rm_reset_password_email.html', {
                'user': self.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
                'token': default_token_generator.make_token(self.user),
            })
            to_email = self.user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            self.regional_manager_id = '1'+str(random.randint(10000,99999))+str(self.pk)
            self.is_verification_email_sent = True

        return super(RegionalManager, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.name

# Custom image upoad path
# def upload_to(instance, filename):
#     return 'business/%s/images/%s' % (instance.user.username, filename)

class Business(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_id  = models.CharField(max_length=100, blank=True)
    regional_manager = models.ForeignKey(RegionalManager, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    domain_name = DomainNameField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = ChainedForeignKey(
            State,
            chained_field="country",
            chained_model_field="country",
            show_all=False,
            auto_choose=True,
            sort=True
        )
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    account_activation_date = models.DateField()
    account_expiry_date = models.DateField()
    is_verification_email_sent = models.BooleanField(default=False)
    is_editing = models.BooleanField(default=False, blank=True, editable=False)
    is_account_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'business'
        verbose_name_plural = 'businesses'

    @property
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    # Override save method
    def save(self, *args, **kwargs):
        if self.is_editing == False and self.is_verification_email_sent == False:
            # Send password reset and activation email
            current_site = Site.objects.get_current()
            mail_subject = 'Reset your password and activate your account.'
            message = render_to_string('accounts/biz_reset_password_email.html', {
                'user': self.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
                'token': default_token_generator.make_token(self.user),
                'altocan_siteurl': current_site,
            })
            to_email = self.user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            self.business_id = '2'+str(random.randint(10000,99999))+str(self.pk)
            self.is_verification_email_sent = True



        super(Business, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name


class TaxOnPlan(models.Model):
    user = models.ForeignKey(Business, on_delete=models.CASCADE)
    tax_type = models.CharField(max_length=20)
    tax_value = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.tax_type


# def upload_to(instance, filename):
#     return 'customers/%s/images/%s' % (instance.user.username, filename)

class Customer(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    customer_id     = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pin_code = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = ChainedForeignKey(
            State,
            chained_field="country",
            chained_model_field="country",
            show_all=False,
            auto_choose=True,
            sort=True,
            blank=True,
            null=True,
        )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Override save method
    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        self.customer_id = '3'+str(random.randint(10000,99999))+str(self.user.id)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


class DashboardImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    business_landing_image = models.ImageField(upload_to='accounts/%Y/%m/%d', default='default/dashboard-landing-image.png', blank=True)
    account_manager_landing_image = models.ImageField(upload_to='accounts/%Y/%m/%d', default='default/dashboard-landing-image.png', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name