from django.contrib import admin
from .models import CashOnDelivery, Header, Footer, ContactPage, Homepage, BannerImage, Service, ServiceActivation, StoreFeature, ParallaxBackground, SocialMediaLink, AboutPage, Policy, TermsAndCondition, Topbar, AboutContent, DirectDepositEmail, PaypalConfig


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    list_display = ('homepage', 'title')
    extra = 1


class StoreFeatureInline(admin.TabularInline):
    model = StoreFeature
    list_display = ('homepage', 'title', 'sub_title')
    extra = 1
    max_num = 4


class ParallaxBackgroundInline(admin.TabularInline):
    model = ParallaxBackground
    list_display = ('homepage', 'title')
    extra = 1
    max_num = 1


class HomepageAdmin(admin.ModelAdmin):
    list_display = ('business',)
    inlines = [BannerImageInline, StoreFeatureInline, ParallaxBackgroundInline]


class HeaderAdmin(admin.ModelAdmin):
    list_display = ['business', 'site_title']

class ParallaxBackgroundAdmin(admin.ModelAdmin):
    list_display = ['homepage', 'title', 'button_name']
    max_num = 1


class ContactPageAdmin(admin.ModelAdmin):
    list_display = ['business', 'address_line_1', 'city', 'country', 'state', 'modified_date']

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = ContactPage.objects.all().count()
        if count == 0:
          return True
        return False


class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['business', 'social_media_name', 'link', 'updated_date']



class AboutContentInline(admin.TabularInline):
    model = AboutContent
    extra = 1

class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['business', 'heading']
    inlines = [AboutContentInline]


    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = AboutPage.objects.all().count()
        if count == 0:
          return True
        return False


class PolicyAdmin(admin.ModelAdmin):
    list_display = ['business', 'heading', 'updated_date']

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = Policy.objects.all().count()
        if count == 0:
          return True
        return False


class TermsAndConditionAdmin(admin.ModelAdmin):
    list_display = ['business', 'heading', 'updated_date']

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = TermsAndCondition.objects.all().count()
        if count == 0:
          return True
        return False


class TopbarAdmin(admin.ModelAdmin):
    list_display = ['business', 'modified_date']

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = Topbar.objects.all().count()
        if count == 0:
          return True
        return False


class DirectDepositEmailAdmin(admin.ModelAdmin):
    list_display = ['business', 'direct_deposit_email', 'is_enabled', 'modified_date']


class PaypalConfigAdmin(admin.ModelAdmin):
    list_display = ['business', 'paypal_client_id', 'is_enabled', 'modified_date']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['business', 'title', 'is_active', 'modified_date']


class ServiceActivationAdmin(admin.ModelAdmin):
    list_display = ('business','is_enabled', 'updated_on')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = ServiceActivation.objects.all().count()
        if count == 0:
          return True
        return False

class CashOnDeliveryAdmin(admin.ModelAdmin):
    list_display = ('business','is_enabled')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = CashOnDelivery.objects.all().count()
        if count == 0:
          return True
        return False


admin.site.register(Header, HeaderAdmin)
admin.site.register(Footer)
admin.site.register(ContactPage, ContactPageAdmin)
admin.site.register(Homepage, HomepageAdmin)
admin.site.register(BannerImage)
admin.site.register(ParallaxBackground, ParallaxBackgroundAdmin)
admin.site.register(StoreFeature)
admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(TermsAndCondition, TermsAndConditionAdmin)
admin.site.register(Topbar, TopbarAdmin)
admin.site.register(AboutContent)
admin.site.register(DirectDepositEmail, DirectDepositEmailAdmin)
admin.site.register(PaypalConfig, PaypalConfigAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceActivation, ServiceActivationAdmin)
admin.site.register(CashOnDelivery, CashOnDeliveryAdmin)
