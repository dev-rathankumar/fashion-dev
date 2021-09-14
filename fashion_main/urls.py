import django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from carts import views as CartViews
from accounts import views as AccountViews
from newsletters import views as NewsletterViews
from products import views as ProductViews
from contacts import views as ContactViews
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += i18n_patterns (
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('', include('pages.urls')),


    # Users
    path('userLogin/', AccountViews.userLogin, name='userLogin'),
    path('userDashboard/', AccountViews.userDashboard, name='userDashboard'),
    path('userDashboard/user/edit/<int:pk>/', AccountViews.editUser, name='editUser'),
    path('userInquiry/', AccountViews.userInquiry, name='userInquiry'),
    path('myOrders/', AccountViews.myOrders, name='myOrders'),
    path('orderDetail/<int:pk>/', AccountViews.orderDetail, name='orderDetail'),
    path('changeuserPassword/', AccountViews.changeuserPassword, name='changeuserPassword'),
    path('userRegister/', AccountViews.userRegister, name='userRegister'),
    path('logout/', AccountViews.logout, name='logout'),
    path('activate/<uidb64>/<token>/', AccountViews.activate, name='activate'),
    path('forgotPassword/', AccountViews.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', AccountViews.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', AccountViews.resetPassword, name='resetPassword'),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Regional Managers
    path('regional_managers/', include('regional_managers.urls')),

    # Business
    path('business/', include('business.urls')),

    # Smart select field
    path('chaining/', include('smart_selects.urls')),

    # Shop
    path('shop/', include('products.urls')),

    # Cart
    path('cart/', include('carts.urls')),
    path('shopcart/', CartViews.shopcart, name='shopcart'),

    # Checkout
    path('checkout/', CartViews.checkout, name='checkout'),

    # Ajax color
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('ajaxVarUrl/', views.ajaxVarUrl, name='ajaxVarUrl'),

    # Newsletters
    path('subscribe/', NewsletterViews.email_list_subscribe, name='subscribe'),

    # Wishlist
    path('my-wishlist/', ProductViews.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', ProductViews.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_addtoshopcart/<int:product_id>/', ProductViews.wishlist_addtoshopcart, name='wishlist_addtoshopcart'),
    path('wishlist_delete/<int:id>/', ProductViews.wishlist_delete, name='wishlist_delete'),

    # Search
    path('search/', ProductViews.search, name='search'),

    # Review
    path('submit_review/<int:product_id>/', ProductViews.submit_review, name='submit_review'),

    # Comparision
    path('compare-products/', ProductViews.compare_products, name='compare_products'),
    path('add_to_compare/<int:product_id>/', ProductViews.add_to_compare, name='add_to_compare'),
    path('remove_from_compare/<int:product_id>/', ProductViews.remove_from_compare, name='remove_from_compare'),

    # Inquiry
    path('inquiry/', ContactViews.inquiry, name="inquiry"),
    path('contact/', ContactViews.contact, name="contact"),
    path('verify_otp/', ContactViews.verify_otp, name='verify_otp'),
    path('resend_otp/', ContactViews.resend_otp, name='resend_otp'),

    # Orders
    path('order/', include('orders.urls')),

    # New Tax
    path('fetchTax/', include('taxes.urls')),

    # Font Awesome Icon Picker
    path('faicon/', include('faicon.urls')),

    #blog
    path('blogs/', include('blogs.urls'))


 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
