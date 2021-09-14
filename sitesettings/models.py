from django.db import models
from django.db.models.base import Model
from accounts.models import Business, User, Country, State
from PIL import Image
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from smart_selects.db_fields import ChainedForeignKey
from faicon.fields import FAIconField


class Header(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    site_title = models.CharField(max_length=500)
    site_logo = models.ImageField(upload_to='logos', blank=True)
    favicon = models.ImageField(upload_to='logos', blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.business


class Homepage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name


class BannerImage(models.Model):
    align_choice = (
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    )
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='banner_images', blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    sub_title = models.CharField(max_length=500, null=True, blank=True)
    button_name = models.CharField(max_length=20, null=True, blank=True)
    button_link = models.CharField(max_length=255, null=True, blank=True)
    button_color = ColorField(default='#000000')
    content_align = models.CharField(max_length=10, choices=align_choice, default='center')

    def __str__(self):
        return self.title


class StoreFeature(models.Model):
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='store_feature_icons', blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    sub_title = models.CharField(max_length=30, null=True, blank=True)
    feature_url = models.URLField(max_length=200, blank = True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.icon.path)

    #     if img.height > 80 or img.weight > 80:
    #         output_size = (80,80)
    #         img.thumbnail(output_size)
    #         img.save(self.icon.path)


    def __str__(self):
        return self.title


class ParallaxBackground(models.Model):
    btn_align_choice = (
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    )
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE)
    parallax_image = models.ImageField(upload_to='parallax_image', blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    button_name = models.CharField(max_length=20, null=True, blank=True)
    button_link = models.CharField(max_length=500, null=True, blank=True)
    button_color = ColorField(default='#000000')
    content_align = models.CharField(max_length=10, choices=btn_align_choice, default='center')

    def __unicode__(self):
        return self.title


class Footer(models.Model):
    ALIGN = (
    ('left','LEFT'),
    ('center', 'CENTER'),
    ('right','RIGHT'),
)

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    footer_text = models.CharField(max_length=500, blank=True)
    hard_code_footer = models.CharField(max_length=100, default='Provided by', blank=True)
    hard_code_branding = models.CharField(max_length=100, default='Altocan', blank=True)
    hard_code_url = models.URLField(default='https://www.altocan.com/', blank=True)
    footer_align = models.CharField(max_length=10, choices=ALIGN, default='center')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.business.company_name


class ContactPage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
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
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    embed_google_map = models.CharField(max_length=1000, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date   = models.DateTimeField(auto_now=True, blank=True)

    @property
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.business.company_name


class SocialMediaLink(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    social_media_name = models.CharField(max_length=50)
    icon = FAIconField()
    link = models.URLField(max_length=500)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date   = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return self.business.company_name


class AboutPage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    sub_heading = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.heading

    
class AboutContent(models.Model):
    about = models.ForeignKey(AboutPage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about/', blank=True)
    header = models.CharField(max_length=255, blank=True)
    header_text = RichTextField(blank=True, null=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date   = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.header


class Policy(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    content = RichTextField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date   = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.heading


class TermsAndCondition(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    content = RichTextField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True)
    updated_date   = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.heading


class Topbar(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    topbar_text = RichTextField(blank=True)
    is_enabled = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name


class DirectDepositEmail(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    direct_deposit_email = models.EmailField(max_length=50, blank=True)
    is_enabled = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.direct_deposit_email


class PaypalConfig(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    paypal_client_id = models.CharField(max_length=150, blank=True)
    is_enabled = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paypal_client_id


class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ServiceActivation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.business.company_name


class CashOnDelivery(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name