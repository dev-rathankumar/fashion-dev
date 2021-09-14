from django.db import models
from category.models import Category
from accounts.models import Business
from accounts.models import User
from django.urls import reverse
from django.forms import ModelForm
from ckeditor.fields import RichTextField
from django.db.models import Avg, Count
from colorfield.fields import ColorField
from smart_selects.db_fields import ChainedForeignKey

# Image manipulation
from io import BytesIO
from PIL import Image
from django.core.files import File

from django.utils.safestring import mark_safe


# Image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image


class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
        ('Custom', 'Custom'),

    )
    business        = models.ForeignKey(Business, on_delete=models.CASCADE)
    product_name    = models.CharField(max_length=200)
    slug            = models.SlugField(max_length=200, unique=True, blank=True)
    description     = RichTextField()
    full_specification = RichTextField(blank=True, default='')
    price           = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)
    image           = models.ImageField(upload_to='store/products/%Y/%m/%d')
    image_2         = models.ImageField(upload_to='store/products/%Y/%m/%d', blank=True, default='default/default-user.png')
    stock           = models.IntegerField(blank=True, null = True)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    variant         = models.CharField(max_length=10,choices=VARIANTS, default='None')
    is_new_arrival  = models.BooleanField(default=False, blank=True)
    is_popular      = models.BooleanField(default=False, blank=True)
    is_active       = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    # Override save method
    def save(self, *args, **kwargs):
        # new_image = compress(self.image)
        # self.image = new_image
        super(Product, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (250,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def avaregereview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(avarage=Avg('rating'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='store/products/%Y/%m/%d', max_length=5000)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = ColorField(default='#000000')

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    attribute_name = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        return self.attribute_name

class AttributeValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, blank=True)
    attribute_value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.attribute_value


def variant_data_default():
    return {'variant_data': 0}

# PRODUCT VARIATION
class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    variant_data = models.JSONField(default=variant_data_default, blank=True, help_text = 'Data should be in JSON format: {"attribute_name": "attribute_value", "attribute_name": "attribute_value"}')
    image_id = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return self.id

    def image(self):
        img = ProductGallery.objects.get(id=self.image_id)
        if img.id is not None:
            varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = ProductGallery.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.product_name

    @property
    def price(self):
        return (self.variant.price)

    @property
    def size(self):
        return (self.variant.size)

    @property
    def color(self):
        return (self.variant.color)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ['quantity']


# Review and Rating model
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(max_length=10, default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    @property
    def business(self):
        return self.product.business


class ReviewForm(ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']


# Comparision model
class Compare(models.Model):
    compare_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.compare_id


class CompareItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    compare    = models.ForeignKey(Compare, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name


class ProductActivation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.business.company_name


class SalesPopup(models.Model):
    INTERVAL_CHOICE = (
        ('Seconds', 'Seconds'),
        ('Minutes', 'Minutes'),
        ('Hours', 'Hours'),
        ('Days', 'Days'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    time = models.CharField(max_length=9)
    interval = models.CharField(max_length=50, choices=INTERVAL_CHOICE, default='Seconds')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.product.product_name


class SalesPopupSetting(models.Model):
    POSITION_CHOICE = (
        ('Left Bottom Corner', 'Left Bottom Corner'),
        ('Right Bottom Corner', 'Right Bottom Corner'),
        ('Left Top Corner', 'Left Top Corner'),
        ('Right Top Corner', 'Right Top Corner'),
    )
    STYLE_CHOICE = (
        ('Rounded', 'Rounded'),
        ('Rectangled', 'Rectangled'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    background_color = ColorField(default='#000000')
    text_color = ColorField(default='#FFFFFF')
    notification_position = models.CharField(max_length=50, choices=POSITION_CHOICE, default='Left Bottom Corner')
    notification_style = models.CharField(max_length=50, choices=STYLE_CHOICE, default='Rounded')
    

    def __str__(self):
        return self.business.company_name