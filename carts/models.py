from django.db import models
from products.models import Product, Variants
from accounts.models import Business, User
from django.forms import ModelForm



class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

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
        product = Product.objects.get(pk=self.product.id)
        if product.variant != 'None':
            return (self.quantity * self.variant.price)
        else:
            return (self.quantity * self.product.price)

    @property
    def varamount(self):
        product = Product.objects.get(pk=self.product.id)
        if product.variant != 'None':
            return (self.quantity * self.variant.price)
        else:
            return (self.quantity * product.price)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Tax(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, unique=True)
    # tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Tax (%)")

    class Meta:
        verbose_name = 'tax'
        verbose_name_plural = 'tax'

    def __unicode__(self):
        return self.business


class TaxSetting(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    tax_type = models.CharField(max_length=20)
    tax_value = models.DecimalField(decimal_places=2, max_digits=4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tax_type
