from django.db import models
from accounts.models import Country, State, Business
from smart_selects.db_fields import ChainedForeignKey


class TaxOnProduct(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, unique=True)

    def __unicode__(self):
        return self.business


class TaxData(models.Model):
    tax_on_product = models.ForeignKey(TaxOnProduct, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = ChainedForeignKey(
            State,
            chained_field="country",
            chained_model_field="country",
            show_all=False,
            auto_choose=True,
            sort=True
        )
    tax_value = models.DecimalField(decimal_places=2, max_digits=4)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tax_on_product
