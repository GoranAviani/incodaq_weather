from __future__ import absolute_import, unicode_literals
from incodaq_weather.celery import app 
from celery import shared_task
import os
darkSkyToken = os.environ.get("darkSkyToken", '')
from api_relay.making_requests import make_request_params
import requests
import json
from incodaq_weather.choice import INDEX_PAGE_CITIES



#testing if this kind of calling already made view functions will work 
@shared_task
def send_daily_forecast_celery(user, typeOfRequest):
    #Solution for avoiding circular importing for this testing
    from .views import send_daily_forecast
    send_daily_forecast(user, typeOfRequest)

@shared_task
def get_periodic_forecast_for_default_cities():
    for x in INDEX_PAGE_CITIES:
        resultForecastRaw = []
        result = {}

        for k, v in x.items():
            city = k
            lat = v["lat"]
            lon = v["lon"]

            #params =  {"params1":{'units': "auto","exclude":"minutely,hourly,daily,alerts,flags"}}
            data =  {'userLat': lat,"userLong": lon, "params":{'units': "si","exclude":"minutely,hourly,daily,alerts,flags"}}           
            asyncForecast = get_default_cities_forecast_dark_sky.delay(**data)
            resultForecastRaw.append(asyncForecast)   

  
    for x in range(0, len(INDEX_PAGE_CITIES)):
        # print(INDEX_PAGE_CITIES[x])
        for key in INDEX_PAGE_CITIES[x]:
            resultForecast = resultForecastRaw[x].get()
             #  print(resultForecast)
            temperature = resultForecast["currently"]["temperature"]
            result[key] = temperature
         
    print("THIS IS THE TEST RESULT" + str(result))