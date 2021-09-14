from accounts.models import Business
from urllib.parse import urlparse
from .models import SalesPopup, SalesPopupSetting, Wishlist, Product, Size, Color, Variants
from django.db.models import Max, Min
from products.models import Compare, CompareItem
from carts.views import _cart_id
from django.db.models import Q

def wish_counter(request):
    current_user = request.user
    wish_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.all().filter(user_id=current_user.id)
            for wish in wishlist:
                wish_count += 1
        except Wishlist.DoesNotExist:
            wish_count = 0
    return dict(wish_count=wish_count)

def compare_counter_header(request):
    compare_count2 = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            compare = Compare.objects.filter(compare_id=_cart_id(request))
            compare_items = CompareItem.objects.all().filter(compare=compare[:1])
            compare_count2 = compare_items.count()
        except Compare.DoesNotExist:
            compare_count2 = 0
    return dict(compare_count2=compare_count2)

def max_product_price(request):
    get_max_price = Product.objects.aggregate(Max('price'))
    try:
        for k,v in get_max_price.items():
            max_price = int(v)
        get_min_price = Product.objects.aggregate(Min('price'))
        for k,v in get_min_price.items():
            min_price = int(v)
    except:
        min_price = 0
        max_price = 0
    return dict(min_price=min_price, max_price=max_price)


def search_products(request):
    products = None
    product_count = 0

    sizes = Size.objects.values_list('name', flat=True).distinct()
    colors = Color.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    if 'min-price' in request.GET:
        min_price = request.GET['min-price']
        max_price = request.GET['max-price']
        if max_price:
            products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
            product_count = products.count()

    if 'size' in request.GET:
        size = request.GET.getlist('size') # ['M', 'XL']
        size_id = Size.objects.filter(name__in=size).values_list('id', flat=True)  # [2, 3, 4]
        product = Variants.objects.filter(size__in=size_id).values_list('product', flat=True)  # [ 1, 2 ]
        products = Product.objects.filter(id__in=product)
        product_count = products.count()

    if 'color' in request.GET:
        color = request.GET.getlist('color')
        color_id = Color.objects.filter(name__in=color).values_list('id', flat=True)  # [2, 3, 4]
        product = Variants.objects.filter(color__in=color_id).values_list('product', flat=True)  # [ 1, 2 ]
        products = Product.objects.filter(id__in=product)
        product_count = products.count()

    # context = {
    #     'products': products,
    #     'product_count': product_count,
    #     'sizes': sizes,
    #     'colors': colors,
    #     'values' : request.GET,
    # }

    return dict(products=products, product_count=product_count, sizes=sizes, colors=colors, values=request.GET)
    # return render(request, 'shop/shop.html', context)


def sales_popup(request):
    
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        popups = SalesPopup.objects.filter(is_active=True)
        popupsettings = SalesPopupSetting.objects.get(business=business)
    except:
        popups = None
        popupsettings = None
    return dict(popups=popups, popupsettings=popupsettings)
    