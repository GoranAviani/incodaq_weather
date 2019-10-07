from celery import shared_task
from weather.views import send_daily_forecast


#testing if this kind of calling already made view functions will work 
@shared_task
def send_daily_forecast_celery(user, typeOfRequest):
    send_daily_forecast(user, typeOfRequest)