from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.banners),
    # Header
    path('header/', views.header, name='header'),
    path('header/add/', views.headerAdd, name='headerAdd'),
    path('header/edit/<int:pk>/', views.headerEdit, name='headerEdit'),
    # Banners
    path('banners/', views.banners, name='banners'),
    path('banners/addBanner/', views.addBanner, name='addBanner'),
    path('banners/editBanner/<int:pk>/', views.editBanner, name='editBanner'),
    path('banners/deleteBanner/<int:pk>/', views.deleteBanner, name='deleteBanner'),

    # Store features
    path('store_features/', views.store_features, name='store_features'),
    path('store_features/addFeature/', views.addFeature, name='addFeature'),
    path('store_features/editFeature/<int:pk>/', views.editFeature, name='editFeature'),
    path('store_features/deleteFeature/<int:pk>/', views.deleteFeature, name='deleteFeature'),

    # Homepage Background
    path('homepage_background/', views.homepage_background, name='homepage_background'),

    # Footer
    path('footerEdit/', views.footerEdit, name='footerEdit'),

    # Topbar
    path('topbarEdit/', views.topbarEdit, name='topbarEdit'),
    path('topbarEdit/topbarToggleEnable/', views.topbarToggleEnable, name='topbarToggleEnable'),

    # Social Icons
    path('socialIcons/', views.socialIcons, name='socialIcons'),
    path('socialIcons/addIcon/', views.addIcon, name='addIcon'),
    path('socialIcons/editIcon/<int:pk>/', views.editIcon, name='editIcon'),
    path('socialIcons/deleteIcon/<int:pk>/', views.deleteIcon, name='deleteIcon'),

    # Pages
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('aboutContent/', views.aboutContent, name='aboutContent'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('editPolicy/', views.editPolicy, name='editPolicy'),
    path('editTermsConditions/', views.editTermsConditions, name='editTermsConditions'),

    path('paymentGateways/', views.paymentGateways, name='paymentGateways'),
    path('paymentGateways/ddToggleEnable/', views.ddToggleEnable, name='ddToggleEnable'),
    path('paymentGateways/ppToggleEnable/', views.ppToggleEnable, name='ppToggleEnable'),
    path('paymentGateways/codToggleEnable/', views.codToggleEnable, name='codToggleEnable'),

    # Store locations
    path('store_locations/', views.store_locations, name='store_locations'),
    path('store_locations/addLocation/', views.addLocation, name='addLocation'),
    path('store_locations/editLocation/<int:pk>/', views.editLocation, name='editLocation'),
    path('store_locations/deleteLocation/<int:pk>/', views.deleteLocation, name='deleteLocation'),

    # Sales Popup
    path('salesPopup/', views.salesPopup, name='salesPopup'),
    path('salesPopup/addPopup/', views.addPopup, name='addPopup'),
    path('salesPopup/editPopup/<int:pk>/', views.editPopup, name='editPopup'),
    path('salesPopup/deletePopup/<int:pk>/', views.deletePopup, name='deletePopup'),

    # Sales Popup Settings
    path('salesPopupSettings/', views.salesPopupSettings, name='salesPopupSettings'),
]
