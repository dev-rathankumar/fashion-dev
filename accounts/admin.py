from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Country, State, Business, RegionalManager, TaxOnPlan, DashboardImage
from django.utils.html import format_html
from django.db.models import Q


# User Admin
class UserAdmin(UserAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;" />'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'

    list_display = ('thumbnail', 'email', 'name', 'username', 'is_customer', 'is_business', 'is_regional_manager', 'is_active', 'is_superadmin')
    list_display_links = ('email', 'name', 'username')
    list_editable = ('is_active',)
    search_fields = ('id', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined', 'is_superadmin', 'is_active')
    ordering = ('-date_joined',)
    exclude = ('is_admin', 'is_staff', 'is_business', 'is_regional_manager', 'is_customer')

    filter_horizontal = ()
    list_filter = ('is_customer','is_business','is_regional_manager','is_active')
    fieldsets = ()


# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'get_name', 'get_email', 'get_status')
    list_display_links = ('customer_id', 'get_name', 'get_email')
    readonly_fields = ['customer_id']


    def get_name(self, obj):
        return obj.user.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def get_status(self, obj):
        return obj.user.is_active
    get_status.short_description = 'Is Active'
    get_status.admin_order_field = 'user__status'


class TaxOnPlanInline(admin.TabularInline):
    model = TaxOnPlan
    list_display = ('user',)
    extra = 1


# Business Admin
class BusinessAdmin(admin.ModelAdmin):
    list_display_links = ('business_id', 'get_name', 'domain_name', 'get_email')
    list_display = ('business_id', 'get_name', 'domain_name', 'get_email', 'get_status')
    readonly_fields = ['business_id']
    inlines = [TaxOnPlanInline]

    def get_name(self, obj):
        return obj.user.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def get_status(self, obj):
        return obj.user.is_active
    get_status.short_description = 'Is Active'
    get_status.admin_order_field = 'user__status'

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = Business.objects.all().count()
        if count == 0:
          return True
        return False

    # ForeignKey list only non-business accounts
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['user'].queryset = User.objects.filter(Q(is_regional_manager=False, is_business=False, is_customer=False, is_superadmin=False, is_active=False) | Q(is_business=True))
         return super(BusinessAdmin, self).render_change_form(request, context, *args, **kwargs)

# Regional Manager Admin
class RegionalManagerAdmin(admin.ModelAdmin):
    list_display_links = ('regional_manager_id', 'get_name', 'get_email')
    list_display = ('regional_manager_id', 'get_name', 'get_email', 'commission_percentage', 'is_verification_email_sent', 'is_account_verified', 'get_status')
    readonly_fields = ['regional_manager_id']

    def get_name(self, obj):
        return obj.user.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def get_status(self, obj):
        return obj.user.is_active
    get_status.short_description = 'Is Active'
    get_status.admin_order_field = 'user__status'

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = RegionalManager.objects.all().count()
        if count == 0:
          return True

        return False


# State Admin
class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'country')
    list_display_links = ('state_name',)
    list_filter = ('country',)
    search_fields = ('state_name',)


class DashboardImageAdmin(admin.ModelAdmin):
    list_display = ('business', 'modified_date')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = DashboardImage.objects.all().count()
        if count == 0:
          return True
        return False



# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Country)
admin.site.register(State, StateAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(RegionalManager, RegionalManagerAdmin)
admin.site.register(DashboardImage, DashboardImageAdmin)
