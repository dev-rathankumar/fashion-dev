from django.urls import path
from . import views


urlpatterns = [
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('saveDDPayment/', views.saveDDPayment, name='saveDDPayment'),
    path('codPlaceOrder/', views.codPlaceOrder, name='codPlaceOrder'),
    path('payments/', views.payments, name="payments"),
    path('order_complete/', views.order_complete, name='order_complete'),

]
