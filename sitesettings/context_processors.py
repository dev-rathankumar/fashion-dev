from sitesettings.models import PaypalConfig
from urllib.parse import urlparse
from accounts.models import Business



def getPaypalClientId(request):
    
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        paypal_config = PaypalConfig.objects.get(business=business)
    except:
        paypal_config = None
    return dict(paypal_config=paypal_config)