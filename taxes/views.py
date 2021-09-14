from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import TaxData
from accounts.models import State
from carts.models import ShopCart



def taxByState(request):
    state_id = request.GET['state_id']
    if request.is_ajax():
        total=0
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        for i in shopcart:
            if i.product.variant == 'None':
                total += i.product.price * i.quantity
            else:
                total += i.variant.price * i.quantity
        try:
            state = State.objects.get(pk=state_id)
            tax_percent = TaxData.objects.get(state=state)
            tx_amount = round((tax_percent.tax_value * total)/100, 2)
            grand_total = round(total + tx_amount, 2)
            data = {
                'state': state.state_name,
                'tax_percent': tax_percent.tax_value,
                'tx_amount': tx_amount,
                'grand_total': grand_total,
            }
            return JsonResponse(data)
        except:
            data = {
                'tax_percent': 0,
                'tx_amount': 0,
                'grand_total': total,
            }
            return JsonResponse(data)
    return HttpResponse('Invalid request')
