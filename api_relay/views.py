from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from incodaq_weather.local_settings import locationiqTokenKey, darkSkyToken, twilioAccountSid, twilioAuthToken, myTwilioTelephone
from django.conf import settings

import os
import logging
#locationiqTokenKey = os.environ.get("locationiqTokenKey", '')
#darkSkyToken = os.environ.get("darkSkyToken", '')
#twilioAccountSid = os.environ.get("twilioAccountSid", '')
#twilioAuthToken = os.environ.get("twilioAuthToken", '')
#myTwilioTelephone = os.environ.get("myTwilioTelephone", '')

# Create your views here.
#This is the place where api functions are getting called from

from .making_requests import make_request_params, twilio_api, make_request

#returning users latitude and longitude
def get_user_lat_long_api(stringToSend):
    apiUrl = {"apiUrl": "https://eu1.locationiq.com/v1/"}
    apiEndpoint = {"apiEndpoint": "search.php"}
    params =  {"params":{'key': locationiqTokenKey,
        'q': stringToSend,
        'format': 'json'}}
    # TODO depreciated due to make_requests
    result = make_request_params(**apiUrl, **apiEndpoint, **params)
    
    try:
        userLat = result[0]["lat"]
        userLon = result[0]["lon"]
        return "success", userLat, userLon
    except:
        return "Can not retrieve latitude and longitude for this place...","",""

def get_user_weather_forecast_api(**kwargs):
    try:
        userLen = kwargs["userLat"]
        userLong = kwargs["userLong"]
        params = {}
        params["params"] = kwargs["params"]
    except:
        return "error"
    apiUrl = {"apiUrl": "https://api.darksky.net/forecast/"}
    apiEndpoint = {"apiEndpoint": darkSkyToken + "/" + userLen +","+userLong}
    # TODO depreciated due to make_requests
    result = make_request_params(**apiUrl, **apiEndpoint, **params) 
    return result

def send_sms_message_api(userMobileNumber, processedForecastMessage):
    twilio_api(userMobileNumber, processedForecastMessage, twilioAccountSid, twilioAuthToken, myTwilioTelephone)

def get_recaptcha_api(recaptcha_response):
    ''' Begin reCAPTCHA validation '''
    sourceOfCall = {"sourceOfCall": "rechaptcha"}
    apiUrl = {"apiUrl": "https://www.google.com/"}
    apiEndpoint = {"apiEndpoint": "recaptcha/api/siteverify"}
    paramsData = {"paramsData": "data"}
    getPost = {"getPost": "post"}
    data = {"data": {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }}
    result = make_request(**apiUrl, **apiEndpoint, **paramsData, **getPost, **data, **sourceOfCall)
    return result
    ''' End reCAPTCHA validation '''
