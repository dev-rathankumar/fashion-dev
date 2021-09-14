from django.db import models
from accounts.models import User, Business


class PaymentSetting(models.Model):
    payment_method_choice = (
        ('PayPal', 'PayPal'),
        ('Bank Account', 'Bank Account'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=payment_method_choice, blank=True)
    paypal_address = models.EmailField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    bank_account_name = models.CharField(max_length=50, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_code = models.CharField(max_length=50, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name
