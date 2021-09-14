from django.urls import path
from . import views

urlpatterns = [
    # Regional Manager activation
    path('rm-password-reset/', views.rm_password_reset, name="rm_password_reset" ),
    path('rm-password-reset-validate/<uidb64>/<token>/', views.rm_password_reset_validate, name='rm_password_reset_validate'),

    # Business activation
    path('biz-password-reset/', views.biz_password_reset, name="biz_password_reset" ),
    path('biz-password-reset-validate/<uidb64>/<token>/', views.biz_password_reset_validate, name='biz_password_reset_validate'),

    # User profile edit
    # path('user/edit/<int:pk>/', views.editUser, name='editUser'),
]
