from portfolio.models import Portfolio, PortfolioActivation, PortfolioGallery, PortfolioHeader
from django.contrib import admin
from django.utils.html import format_html
import admin_thumbnails


class PortfolioHeaderAdmin(admin.ModelAdmin):
    list_display = ('business', 'heading', 'sub_heading')
    def has_add_permission(self, request):
        count = PortfolioHeader.objects.all().count()
        if count == 0:
          return True
        return False


class PortfolioGalleryAdmin(admin.StackedInline):
    model =  PortfolioGallery


@admin_thumbnails.thumbnail('image')
class PortfolioGalleryInline(admin.TabularInline):
    model = PortfolioGallery
    readonly_fields = ('id',)
    extra = 1


class PortfolioAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;" />'.format(object.featured_image.url))
    thumbnail.short_description = 'Image'
    list_display = ('thumbnail', 'business', 'title', 'modified_date')
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('thumbnail', 'business', 'title')
    search_fields = ('id', 'title')
    inlines = [PortfolioGalleryInline]

    class Meta:
        model=Portfolio


class PortfolioActivationAdmin(admin.ModelAdmin):
    list_display = ('business','is_enabled', 'updated_on')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = PortfolioActivation.objects.all().count()
        if count == 0:
          return True
        return False

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioGallery)
admin.site.register(PortfolioHeader, PortfolioHeaderAdmin)
admin.site.register(PortfolioActivation, PortfolioActivationAdmin)
