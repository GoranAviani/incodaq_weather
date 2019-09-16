from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.edit_user_phone, name='edit_mobile_phone'),
    
]