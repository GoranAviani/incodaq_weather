from __future__ import absolute_import, unicode_literals
from incodaq_weather.celery import app 
from celery import shared_task
import os
from api_relay.making_requests import make_request_params
import requests
import json
from incodaq_weather.choice import INDEX_PAGE_CITIES
from weather.models import (
    default_cities
)
darkSkyToken = os.environ.get("darkSkyToken", '')


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
    from .views import process_forecast_api_message
    result = {}

    for x in INDEX_PAGE_CITIES:        
        for k, v in x.items():
            city = k
            lat = v["lat"]
            lon = v["lon"]

            params = {'units': "si", "exclude": "minutely,hourly,daily,alerts,flags"}

            apiUrl = "https://api.darksky.net/forecast/"
            apiEndpoint = darkSkyToken + "/" + lat +","+lon
            fullAPIUrl = apiUrl + apiEndpoint
            apiResponse = requests.get(fullAPIUrl, params=params)
            apiResponse = apiResponse.json()

            data = {'typeOfCall': "basic_forecast", "apiResponse": apiResponse}
            processedForecastMsgStatus, processedForecastMsg = process_forecast_api_message(**data)
            result[city] = processedForecastMsg

            #<class 'dict'>: {'latitude': 59.3251172, 'longitude': 18.0710935, 'timezone': 'Europe/Stockholm',
            # 'currently': {'time': 1573572991, 'summary': 'Possible Light Rain', 'icon': 'rain', 'precipIntensity':
            # 0.548, 'precipProbability': 0.61, 'precipType': 'rain', 'temperature': 6.02, 'apparentTemperature': 2.33,
            # 'dewPoint': 5.07, 'humidity': 0.94, 'pressure': 1005.1, 'windSpeed': 5.63,
            # 'windGust': 12.5, 'windBearing': 146, 'cloudCover': 0.76, 'uvIndex': 0, 'visibility': 4.174, 'ozone': 303},
            # 'offset': 1}


    print(str(result))
    for city, temp in result.items():
        print("city: {}, temp: {}" .format(city, temp))

   # for x in range(0, len(INDEX_PAGE_CITIES)):
        # print(INDEX_PAGE_CITIES[x])
   #     for key in INDEX_PAGE_CITIES[x]:
   #         resultForecast = resultForecastRaw[x].get()
             #  print(resultForecast)
    #        temperature = resultForecast["currently"]["temperature"]
    #        result[key] = temperature
         
    print("THIS IS THE TEST RESULT" + str(result))

    default_cities.objects.update(Stockholm="13"
                    , Tokyo="45"
                    )

    print("END OF TASK")