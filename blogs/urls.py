from django.urls import path
from . import views

urlpatterns = [

    path('', views.blog, name='blog'),
    path('category/<slug:slug>/', views.blog, name='blogs_by_category'),
    path('<slug:category_slug>/<slug:blog_slug>/', views.blog_detail, name='blog_detail'),
]
