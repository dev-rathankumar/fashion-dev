from .models import ShopCart, Tax, TaxSetting
from .views import _cart_id, shopcart
from category.models import Category
from accounts.models import Business
from urllib.parse import urlparse
from django.db.models import FloatField
from django.db.models.functions import Cast



def counter(request):
    current_user = request.user
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_items = ShopCart.objects.all().filter(user_id=current_user.id)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except ShopCart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)



# Cart method
def shopcart_context(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total=0
    # tax = 0
    # grand_total = 0
    # tax_percent = 0
    for i in shopcart:
        if i.product.variant != 'None':
            total += i.variant.price * i.quantity
        else:
            total += i.product.price * i.quantity

    
    try:
        biz_id = Business.objects.get(user__is_business=True, is_account_verified=True)
    except:
        biz_id = None

    # get_tax = TaxSetting.objects.all()
    # tax_dict = {}
    # for i in get_tax:
    #     tax_type = i.tax_type
    #     tax_value = i.tax_value
    #     tx_amount = round((tax_value * total)/100, 2)
    #     tax_dict.update({tax_type: {float(tax_value):float(tx_amount)}})
    #
    # tax = sum(x for counter in tax_dict.values() for x in counter.values())
    # grand_total = round(float(total) + tax, 2)
    # return dict(shopcart=shopcart, category=category, total=total, tax_percent=tax_percent, tax=tax, grand_total=grand_total, tax_dict=tax_dict)
    return dict(shopcart=shopcart, category=category, total=total)
