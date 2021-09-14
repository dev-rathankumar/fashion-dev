from django.contrib import admin
from .models import TaxOnProduct, TaxData


class TaxDataInline(admin.TabularInline):
    model = TaxData
    extra = 0


class TaxOnProductAdmin(admin.ModelAdmin):
    list_display = ('business',)
    inlines = [TaxDataInline]

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = TaxOnProduct.objects.all().count()
        if count == 0:
          return True
        return False


admin.site.register(TaxOnProduct, TaxOnProductAdmin)
