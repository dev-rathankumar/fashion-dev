from django.contrib import admin
from .models import Category
from products.models import Product
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "category_name"
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;" />'.format(object.cat_image.url))
    thumbnail.short_description = 'Category Image'
    list_display = ('thumbnail', 'tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('thumbnail', 'indented_title',)
    prepopulated_fields = {'slug': ('category_name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'




admin.site.register(Category, CategoryAdmin)
