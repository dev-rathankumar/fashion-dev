from django.db import models

class Plan(models.Model):
    PlanFrequencyChoice = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half-yearly', 'Half-Yearly'),
        ('annually', 'Annually'),
    )
    plan_name = models.CharField(max_length=50)
    plan_frequency = models.CharField(choices=PlanFrequencyChoice, max_length=50)
    plan_price = models.FloatField()
    plan_description = models.TextField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name


class PlanPayment(models.Model):
    business = models.ForeignKey('accounts.Business', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


def tax_data_default():
    return {'tax': 0}

class PlanOrder(models.Model):
    business = models.ForeignKey('accounts.Business', on_delete=models.CASCADE)
    plan_payment = models.ForeignKey(PlanPayment, on_delete=models.SET_NULL, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    total = models.FloatField()
    tax = models.FloatField()
    tax_data = models.JSONField(default=tax_data_default, help_text = "Data format: {'tax_type':{'tax_value':'tax_amount'}}")
    account_manager_commission = models.FloatField()
    ip = models.CharField(blank=True, max_length=20)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.company_name
