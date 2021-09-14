from django.contrib import admin
from .models import Product, ProductActivation, ProductGallery, Color, SalesPopup, SalesPopupSetting, Size, Variants, Wishlist, ReviewRating, Compare, CompareItem, ProductAttribute, AttributeValue
from django.utils.html import format_html
import admin_thumbnails

# Register your models here.

class ProductGalleryAdmin(admin.StackedInline):
    model =  ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    readonly_fields = ('id',)
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 0
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;" />'.format(object.image.url))
    thumbnail.short_description = 'Product Image'
    list_display = ('thumbnail', 'business', 'product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'is_active')
    prepopulated_fields = {'slug': ('product_name',)}
    list_display_links = ('thumbnail', 'business', 'product_name', 'price', 'stock', 'category')
    list_editable = ('is_active','is_available')
    search_fields = ('id', 'product_name', 'category__category_name')
    list_filter = ('category',)
    inlines = [ProductGalleryInline,ProductVariantsInline]

    class Meta:
        model=Product

# @admin.register(ProductGallery)
# class ProductGalleryAdmin(admin.ModelAdmin):
#     pass




class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name',]


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant', 'size', 'color', 'user','quantity','price','amount' ]
    list_filter = ['user']


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'business', 'user', 'subject', 'status', 'create_at', 'update_at']
    readonly_fields = ('product','business','user','subject','review','ip')

class CompareAdmin(admin.ModelAdmin):
    list_display = ['compare_id', 'date_added']

class CompareItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'compare', 'is_active']

class ProductActivationAdmin(admin.ModelAdmin):
    list_display = ('business','is_enabled', 'updated_on')

    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = ProductActivation.objects.all().count()
        if count == 0:
          return True
        return False

class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute_value', 'product_attribute')
    list_display_links = ('attribute_value',)
    list_filter = ('product_attribute',)
    search_fields = ('attribute_value',)

class SalesPopupSettingAdmin(admin.ModelAdmin):
    # if there's already an entry, do not allow adding
    def has_add_permission(self, request):
        count = SalesPopupSetting.objects.all().count()
        if count == 0:
          return True
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Compare, CompareAdmin)
admin.site.register(CompareItem, CompareItemAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductActivation, ProductActivationAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(ProductAttribute)
admin.site.register(SalesPopup)
admin.site.register(SalesPopupSetting, SalesPopupSettingAdmin)
