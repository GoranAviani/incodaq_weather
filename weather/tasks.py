from __future__ import absolute_import, unicode_literals
from incodaq_weather.celery import app 
from celery import shared_task
import os
darkSkyToken = os.environ.get("darkSkyToken", '')
from api_relay.making_requests import make_request_params
import requests
import json

#testing if this kind of calling already made view functions will work 
@shared_task
def send_daily_forecast_celery(user, typeOfRequest):
    #Solution for avoiding circular importing for this testing
    from .views import send_daily_forecast
    send_daily_forecast(user, typeOfRequest)


@shared_task
def get_user_weather_forecast_dark_sky(**kwargs):
    userLen = kwargs["userLat"]
    userLong = kwargs["userLong"]
    #params = {}
    #params["params"] = kwargs["params"]
    params = kwargs["params"]
    
    apiUrl = "https://api.darksky.net/forecast/"
    apiEndpoint = darkSkyToken + "/" + userLen +","+userLong
    #result = make_request_params(**apiUrl, **apiEndpoint, **params) 
    fullAPIUrl = apiUrl + apiEndpoint
    result = requests.get(fullAPIUrl, params=params)
    return result.json()
