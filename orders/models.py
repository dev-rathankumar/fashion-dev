from django.db import models
from accounts.models import Business, User, Country, State
from products.models import Product, Variants
from django.forms import ModelForm
from smart_selects.db_fields import ChainedForeignKey



class Payment(models.Model):
    PAYMENT_METHOD = (
        ('paypal', 'PayPal'),
        ('direct deposit', 'Direct Deposit'),
        ('cash on delivery', 'Cash On Delivery'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100, default='paypal')
    amount = models.CharField(max_length=100)
    date_of_dd_payment = models.DateField(blank=True, null=True)
    dd_attachment = models.ImageField(upload_to='direct_deposit_attachments', blank=True, null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


def tax_data_default():
    return {'tax': 0}


class StoreLocation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email           = models.EmailField(max_length=100)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = ChainedForeignKey(
            State,
            chained_field="country",
            chained_model_field="country",
            show_all=False,
            auto_choose=True,
            sort=True
        )
    geolocation = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name

    @property
    def address(self):
        return f'{self.address_line_1} {self.address_line_2}'


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('On Hold', 'On Hold'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    store_location = models.ForeignKey(StoreLocation, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
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
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(default=tax_data_default, blank=True, help_text = "Data format: {'tax_type':{'tax_value':'tax_amount'}}")
    tax = models.FloatField()
    payment_method = models.CharField(max_length=25, default='PayPal')
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(max_length=100, blank=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'note']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('On Hold', 'On Hold'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


    
    
    