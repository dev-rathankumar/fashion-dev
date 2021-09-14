from portfolio.models import Portfolio, PortfolioGallery
from sitesettings.models import Service
from django import forms
from accounts.models import User, Business
from .models import PaymentSetting
from products.models import AttributeValue, Product, ProductAttribute, ProductGallery, Variants, Color, Size
from category.models import Category
from ckeditor.widgets import CKEditorWidget
from django.forms import inlineformset_factory
from mptt.forms import TreeNodeChoiceField
from orders.models import Order
from carts.models import TaxSetting
from blogs.models import Blog
from blogs.models import Category as BlogCategory


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
    }), label="Email")
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "class": "file",
        "type": "file",
        # "data-browse-on-zone-click": "true",
        "data-show-preview": "false"
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'number',
        'maxlength': 12,
        'oninput' : 'javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);',
        'class': 'inputNumber',
    }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_picture']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control file'


class BusinessForm(forms.ModelForm):
    is_editing = forms.BooleanField(widget=forms.HiddenInput(attrs={
        "type": "hidden",
        'value': 'True',
    }), initial=1)
    is_editing = forms.BooleanField(required=False,initial=True)
    

    class Meta:
        model = Business
        fields = ['company_name', 'country', 'state', 'city', 'pin_code', 'address_line_1', 'address_line_2']
        exclude = ('user',)

        # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control'


class PaymentSettingForm(forms.ModelForm):
    CHOICES = (('PayPal', 'PayPal'),('Bank Account', 'Bank Account'),)
    payment_method = forms.CharField(widget=forms.Select(choices=CHOICES))
    class Meta:
        model = PaymentSetting
        fields = ['payment_method', 'paypal_address', 'bank_name', 'bank_account_name', 'bank_account_number', 'bank_code']

        # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(PaymentSettingForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].widget.attrs['onchange'] = 'showDiv(this)'
        for myField in self.fields:
          self.fields[myField].widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(label=('Product Image 01'), required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))
    image_2 = forms.ImageField(label=('Product Image 02'), required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'full_specification', 'price', 'variant', 'image', 'image_2', 'stock', 'category', 'is_popular']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['variant'].widget.attrs['onchange'] = 'showDiv(this)'
        for myField in self.fields:
            if myField == 'is_popular':
                self.fields[myField].widget.attrs['class'] = 'custom-chckbox-is_popular'
            elif myField == 'image' or myField == 'image_2':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'


class ProductGalleryForm(forms.ModelForm):
    image = forms.ImageField(label=('Product Gallery Image'), required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "class": "file",
        # "data-browse-on-zone-click": "true",
        "data-show-preview": "false",
    }))
    class Meta:
        model = ProductGallery
        fields = ('image',)
        exclude = ()


class ProductVariantForm(forms.ModelForm):
    product_attribute = forms.ModelChoiceField(required=False, queryset=ProductAttribute.objects.all())
    attribute_value = forms.ModelChoiceField(required=False, queryset=AttributeValue.objects.all())
    class Meta:
        model = Variants
        fields = ('id', 'title', 'color', 'size', 'product_attribute', 'attribute_value', 'variant_data', 'image_id', 'quantity', 'price')
        exclude = ()

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(ProductVariantForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'image_id':
                self.fields[myField].widget.attrs['class'] = 'form-control image_id'
            if myField == 'variant_data':
                self.fields[myField].widget.attrs['class'] = 'form-control nvvariant'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Category.objects.all())

    cat_image = forms.ImageField(label=('Category Image'), required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))
    class Meta:
        model = Category
        fields = ('category_name', 'parent', 'cat_image', 'description')

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        for myField in self.fields:
            if myField == 'cat_image':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            elif myField == 'description':
                self.fields[myField].widget.attrs['class'] = 'form-control'
                self.fields[myField].widget.attrs['rows'] = '4'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'state', 'country', 'pin_code','note', 'status')
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class TaxSettingForm(forms.ModelForm):
    class Meta:
        model = TaxSetting
        fields = ('tax_type', 'tax_value', 'is_active')
    def __init__(self, *args, **kwargs):
        super(TaxSettingForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name', 'code']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


#addBlogForm
class BlogForm(forms.ModelForm):
    featured_image = forms.ImageField(label=('Blog Image'), required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))

    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'blog_body', 'featured_image',  'category', 'status' ]

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'featured_image':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'

#addBlogCategory
class BlogCategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=BlogCategory.objects.all())

    class Meta:
        model = BlogCategory
        fields = ('category_name', 'parent', 'description')

    # Give same CSS class to all the fields
    def __init__(self, *args, **kwargs):
        super(BlogCategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
        for myField in self.fields:
            if myField == 'cat_image':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            elif myField == 'description':
                self.fields[myField].widget.attrs['class'] = 'form-control'
                self.fields[myField].widget.attrs['rows'] = '4'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'


class ServiceForm(forms.ModelForm):
    image = forms.ImageField(label=('Image'), required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))
    class Meta:
        model = Service
        fields = ['title', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            if myField == 'image':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'



class PortfolioForm(forms.ModelForm):
    featured_image = forms.ImageField(label=('Image'), required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "data-show-preview": "false"
    }))
    class Meta:
        model = Portfolio
        fields = ['title', 'featured_image', 'description', 'live_preview_button', 'button_name', 'button_link', 'button_bg_color', 'button_text_color', 'button_alignment']

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.fields['live_preview_button'].widget.attrs['onchange'] = 'showhideButton()'
        for myField in self.fields:
            if myField == 'featured_image':
                self.fields[myField].widget.attrs['class'] = 'form-control file'
            else:
                self.fields[myField].widget.attrs['class'] = 'form-control'


class PortfolioGalleryForm(forms.ModelForm):
    image = forms.ImageField(label=('Portfolio Gallery Image'), required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={
        "type": "file",
        "class": "file",
        "data-show-preview": "false",
    }))
    class Meta:
        model = PortfolioGallery
        fields = ('image',)
        exclude = ()

    
class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('attribute_name',)
    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['required'] = 'required'


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ('attribute_value', 'product_attribute')
    def __init__(self, *args, **kwargs):
        super(AttributeValueForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['required'] = 'required'