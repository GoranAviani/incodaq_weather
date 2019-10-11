from __future__ import absolute_import, unicode_literals
from incodaq_weather.celery import app 
from celery import shared_task


#testing if this kind of calling already made view functions will work 
@shared_task
def send_daily_forecast_celery(user, typeOfRequest):
    #Solution for avoiding circular importing for this testing
    from .views import send_daily_forecast
    send_daily_forecast(user, typeOfRequest)