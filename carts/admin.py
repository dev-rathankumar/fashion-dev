from django.contrib import admin
from .models import Tax, ShopCart, TaxSetting

# class TaxSettingInline(admin.TabularInline):
#     model = TaxSetting
#     list_display = ('business',)
#     extra = 1


# class TaxAdmin(admin.ModelAdmin):
#     list_display = ('business',)
#     inlines = [TaxSettingInline]


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','amount', 'size', 'color', 'created_at' ]
    list_filter = ['user']


admin.site.register(ShopCart, ShopCartAdmin)
# admin.site.register(Tax, TaxAdmin)
