from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from accounts.models import Business
from django.db import models
from django.urls import reverse


class PortfolioHeader(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100, blank=True)
    sub_heading = models.TextField(max_length=500, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading


class Portfolio(models.Model):
    align_choice = (
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    featured_image = models.ImageField(upload_to='portfolio/')
    description = RichTextField(blank=True, null=True)
    live_preview_button = models.BooleanField(default=False)
    button_name = models.CharField(max_length=20, null=True, blank=True)
    button_link = models.CharField(max_length=500, null=True, blank=True)
    button_bg_color = ColorField(default='#000000', null=True)
    button_text_color = ColorField(default='#FFFFFF', null=True)
    button_alignment = models.CharField(max_length=10, choices=align_choice, default='center', null=True)
    is_active = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('portfolio_detail', args=[self.slug])


class PortfolioGallery(models.Model):
    portfolio = models.ForeignKey(Portfolio, default=None, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='portfolio/%Y/%m/%d', max_length=5000)

    def __str__(self):
        return self.portfolio.title

    class Meta:
        verbose_name = 'portfoliogallery'
        verbose_name_plural = 'portfolio gallery'


class PortfolioActivation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.business.company_name