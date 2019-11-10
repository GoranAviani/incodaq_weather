from __future__ import absolute_import, unicode_literals
from incodaq_weather.celery import app 
from celery import shared_task
import os
darkSkyToken = os.environ.get("darkSkyToken", '')
from api_relay.making_requests import make_request_params
import requests
import json
from incodaq_weather.choice import INDEX_PAGE_CITIES
from weather.models import (
    default_cities
)

#testing if this kind of calling already made view functions will work 
@shared_task
def send_daily_forecast_celery(user, typeOfRequest):
    #Solution for avoiding circular importing for this testing
    from .views import send_daily_forecast
    send_daily_forecast(user, typeOfRequest)

#async task
@shared_task
def get_user_weather_forecast_dark_sky(**kwargs):
    userLen = kwargs["userLat"]
    userLong = kwargs["userLong"]
    #params = {}
    #params["params"] = kwargs["params"]
    params = kwargs["params"]
    
    apiUrl = "https://api.darksky.net/forecast/"
    apiEndpoint = darkSkyToken + "/" + userLen +","+userLong
    fullAPIUrl = apiUrl + apiEndpoint
    result = requests.get(fullAPIUrl, params=params)
    return result.json()


@shared_task
def get_periodic_forecast_for_default_cities():
    resultForecastRaw = []
    result = {}

    for x in INDEX_PAGE_CITIES:        
        for k, v in x.items():
            city = k
            lat = v["lat"]
            lon = v["lon"]

            #params =  {"params1":{'units': "auto","exclude":"minutely,hourly,daily,alerts,flags"}}
            data =  {'userLat': lat,"userLong": lon, "params":{'units': "si","exclude":"minutely,hourly,daily,alerts,flags"}}           
            params = {'units': "si","exclude":"minutely,hourly,daily,alerts,flags"}

            apiUrl = "https://api.darksky.net/forecast/"
            apiEndpoint = darkSkyToken + "/" + lat +","+lon
            fullAPIUrl = apiUrl + apiEndpoint
            result1 = requests.get(fullAPIUrl, params=params)
            result1 = result1.json()
            resultForecastRaw.append(result1)   

            #asyncForecast = get_default_cities_forecast_dark_sky.delay(**data)
            #resultForecastRaw.append(asyncForecast)   
        print("resultforecast RAW               A")
        print(resultForecastRaw)
   # for x in range(0, len(INDEX_PAGE_CITIES)):
        # print(INDEX_PAGE_CITIES[x])
   #     for key in INDEX_PAGE_CITIES[x]:
   #         resultForecast = resultForecastRaw[x].get()
             #  print(resultForecast)
    #        temperature = resultForecast["currently"]["temperature"]
    #        result[key] = temperature
         
    print("THIS IS THE TEST RESULT" + str(result))

    default_cities.objects.update(Stockholm="12"
                    , Tokyo="55"
                    )

    print("END OF TASK")