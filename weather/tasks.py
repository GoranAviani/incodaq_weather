from __future__ import absolute_import, unicode_literals

# import the logging library
import logging

from incodaq_weather.celery import app
from celery import shared_task
import os
from api_relay.making_requests import make_request_params
import requests
import json

from incodaq_weather.choice import INDEX_PAGE_CITIES
from incodaq_weather.processing import rounding_number
from weather.models import (
    default_cities
)
from incodaq_weather.local_settings import darkSkyToken

from expanded_user.models import custom_user
# from .views import send_daily_forecast
from django.http import HttpResponse


# periodic task
@shared_task
def send_daily_forecast_to_all_celery():
    users = custom_user.objects.all()
    typeOfRequest = "autoWeatherRequest"
    # Solution for avoiding circular importing for this testing
    from .views import send_daily_forecast
    for user in users:
        send_daily_forecast(user, typeOfRequest)



# async task
@shared_task
def get_user_weather_forecast_dark_sky(**kwargs):
    userLen = kwargs["userLat"]
    userLong = kwargs["userLong"]
    params = kwargs["params"]

    apiUrl = "https://api.darksky.net/forecast/"
    apiEndpoint = darkSkyToken + "/" + userLen + "," + userLong
    fullAPIUrl = apiUrl + apiEndpoint
    result = requests.get(fullAPIUrl, params=params)
    return result.json()


# periodic task
@shared_task
def get_periodic_forecast_for_default_cities(*args, **kwargs):
    from .views import process_forecast_api_message
    result = []
    for city_info in INDEX_PAGE_CITIES:
        for city_name, city_position in city_info.items():
            city = city_name
            lat = city_position["lat"]
            lon = city_position["lon"]

            params = {'units': "si", "exclude": "minutely,hourly,daily,alerts,flags"}

            apiUrl = "https://api.darksky.net/forecast/"
            apiEndpoint = darkSkyToken + "/" + lat + "," + lon
            fullAPIUrl = apiUrl + apiEndpoint
            apiResponse = requests.get(fullAPIUrl, params=params)
            if apiResponse.status_code not in (200):
                logging.getLogger("darksky_error_logger").error("Dark Sky failed response: %s", apiResponse.json())
                break
            else:
                logging.getLogger("darksky_info_logger").info("Dark Sky successful response: %s", apiResponse.json())

            apiResponse = apiResponse.json()

            data = {'typeOfCall': "default_cities_adv_forecast", "apiResponse": apiResponse}
            processedStatus, processedTemp, processedIconDesc = process_forecast_api_message(**data)
            processedTemp = rounding_number(processedTemp)

            result.append({'city': city, 'temp': processedTemp, 'iconDesc': processedIconDesc})

    for x in result:
        try:
            #try to find the current ciry if it exists already
            found_city_data = default_cities.objects.get(city=x["city"])
            # if found update the temp
            default_cities.objects.filter(city=x["city"]).update(temperature=x["temp"], weatherIconDesc=x["iconDesc"])
        except:
            #if city is not found create it
            default_cities.objects.create(city=x["city"], temperature=x["temp"], weatherIconDesc=x["iconDesc"])



    # if this function has been called from a view
    try:
        if args[0].path == '/weather_app/update_index_statuses/':
            return HttpResponse('Index cities temperature and weather conditions have been updated.')
    except:
        #it is celery task running this fun
        pass