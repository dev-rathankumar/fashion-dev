from django.contrib import admin
from .models import Email, BusinessEmailSetting
from accounts.models import User
from .forms import BusinessEmailSettingForm


class EmailAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['to_address'].queryset = User.objects.filter(is_customer=True, is_active=True)
         return super(EmailAdmin, self).render_change_form(request, context, *args, **kwargs)


class BusinessEmailSettingAdmin(admin.ModelAdmin):
    form = BusinessEmailSettingForm
    list_display = ('business', 'email_host', 'email_host_user', 'is_settings_verified', 'updated_at')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = BusinessEmailSetting.objects.all().count()
        if count == 0:
          return True

        return False


admin.site.register(Email, EmailAdmin)
admin.site.register(BusinessEmailSetting, BusinessEmailSettingAdmin)
