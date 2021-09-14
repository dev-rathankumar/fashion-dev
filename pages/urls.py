from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact_page/', views.contact_page, name='contact_page'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),

    # Services
    path('services/', views.services, name='services'),

    # Portfolio
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:portfolio_slug>/', views.portfolio_detail, name='portfolio_detail'),

]
