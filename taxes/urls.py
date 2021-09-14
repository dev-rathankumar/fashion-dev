from django.urls import path
from . import views


urlpatterns = [
    path('taxByState/', views.taxByState, name='taxByState'),
    ]
