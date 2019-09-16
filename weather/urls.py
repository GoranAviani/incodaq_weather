from django.urls import path
from . import views

urlpatterns = [
    path('send_daily_forecast_to_all/', views.send_daily_forecast_to_all, name='send_daily_forecast'),
    path('send_daily_forecast_to_user/', views.send_daily_forecast_to_user, name='send_daily_forecast_to_user'),
    
]