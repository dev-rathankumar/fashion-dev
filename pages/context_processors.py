from django.http import HttpResponse
from sitesettings.models import ContactPage, SocialMediaLink
from urllib.parse import urlparse
from accounts.models import Business


def social_media_links(request):
    
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
    except:
        business = None
    if business is not None:
        social_icons = SocialMediaLink.objects.filter(business=business).order_by('created_date')
    else:
        social_icons = None
    return dict(social_icons=social_icons)
#
# def social_icons(request):
#     current_user = request.user
#     wish_count = 0
#     if 'admin' in request.path:
#         return {}
#     else:
#         try:
#             wishlist = Wishlist.objects.all().filter(user_id=current_user.id)
#             for wish in wishlist:
#                 wish_count += 1
#         except Wishlist.DoesNotExist:
#             wish_count = 0
#     return dict(wish_count=wish_count)


def address(request):
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        contact_page = ContactPage.objects.get(business=business)
        return dict(contact_page=contact_page)
    except:
        return {}

