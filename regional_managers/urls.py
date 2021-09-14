from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='rm_dashboard'),
    path('login/', views.login, name='rm_login'),
    path('logout/', views.logout, name='rm_logout'),

    path('forgotPassword/', views.forgotPassword, name='rm_forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='rm_resetForgotPassword_validate'),
    path('resetPassword/', views.rm_resetPassword, name='rm_resetForgotPassword'),

    path('profile/', views.rm_profile, name='rm_profile'),
    path('changePassword/', views.rm_changePassword, name='rm_changePassword'),

    # Edit profile
    path('editProfile/<int:pk>/', views.editProfile, name='rm_editProfile'),

    path('supplier/', views.supplier, name='supplier'),
    path('bizPlanPurchaseHistory/', views.bizPlanPurchaseHistory, name='bizPlanPurchaseHistory'),
    path('bizPlanHistoryDetail/<int:pk>/', views.bizPlanHistoryDetail, name='bizPlanHistoryDetail'),

]
