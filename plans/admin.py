from django.contrib import admin
from .models import Plan, PlanOrder, PlanPayment


class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'plan_frequency', 'plan_price', 'modified_date']


class PlanOrderInline(admin.TabularInline):
    model = PlanOrder
    fields = ['order_number', 'business', 'plan_payment', 'plan', 'total', 'tax', 'tax_data', 'account_manager_commission', 'ordered', 'created_at']
    readonly_fields = ['order_number', 'business', 'plan_payment', 'plan', 'total', 'tax', 'tax_data', 'account_manager_commission', 'ordered', 'created_at']
    can_delete = False
    extra = 1


class PlanPaymentAdmin(admin.ModelAdmin):
    list_display = ['business', 'payment_id', 'payment_method', 'amount', 'status', 'created_at']
    readonly_fields = ('business', 'payment_id', 'payment_method', 'amount', 'status', 'created_at')
    inlines = [PlanOrderInline]


admin.site.register(Plan, PlanAdmin)
admin.site.register(PlanPayment, PlanPaymentAdmin)
admin.site.register(PlanOrder)
