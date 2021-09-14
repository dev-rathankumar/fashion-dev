from django.urls import path
from . import views

urlpatterns = [
    # path('', views.category, name='category'),
    path('category/<slug:slug>/', views.shop, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('category/', views.shop),
    path('', views.shop, name='shop'),
]
