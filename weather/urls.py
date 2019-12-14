from django.urls import path
from . import views
from . import tasks

urlpatterns = [
    path('send_daily_forecast_to_all/', views.send_daily_forecast_to_all, name='send_daily_forecast'),
    path('send_daily_forecast_to_user/', views.send_daily_forecast_to_user, name='send_daily_forecast_to_user'),
    path('update_index_statuses/', tasks.get_periodic_forecast_for_default_cities, name='update_index_statuses'),
]