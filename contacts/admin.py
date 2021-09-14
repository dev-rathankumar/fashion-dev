from django.contrib import admin
from .models import Inquiry, SiteContact


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('business', 'first_name', 'last_name', 'product_name', 'email', 'create_date')
    list_display_links = ('business', 'first_name', 'last_name', 'product_name', 'email')


# Contact Admin
class SiteContactAdmin(admin.ModelAdmin):
    list_display = ('get_business_id', 'business', 'name', 'email', 'phone', 'create_date')
    list_display_links = ('get_business_id', 'business', 'name', 'email', 'phone')
    search_fields = ('id', 'business__business_id', 'business', 'name', 'email', 'phone')

    def get_business_id(self, obj):
        return obj.business.business_id
    get_business_id.short_description = 'Business ID'
    get_business_id.admin_order_field = 'business__business_id'


admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(SiteContact, SiteContactAdmin)
