from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),

    # AJAX
    path('add_cart_ajax/<int:product_id>/', views.add_cart_ajax, name='add_cart_ajax'),

    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('addtoshopcart/<int:product_id>/', views.addtoshopcart, name='addtoshopcart'),
    path('delete_itemfromcart/<int:product_id>', views.delete_itemfromcart, name='delete_itemfromcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
]
