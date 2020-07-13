from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from incodaq_weather.local_settings import locationiqTokenKey, darkSkyToken, twilioAccountSid, twilioAuthToken, myTwilioTelephone
from django.conf import settings
from incodaq_weather.constants import API_URLS

import os
import logging
#locationiqTokenKey = os.environ.get("locationiqTokenKey", '')
#darkSkyToken = os.environ.get("darkSkyToken", '')
#twilioAccountSid = os.environ.get("twilioAccountSid", '')
#twilioAuthToken = os.environ.get("twilioAuthToken", '')
#myTwilioTelephone = os.environ.get("myTwilioTelephone", '')

# Create your views here.
#This is the place where api functions are getting called from

from .making_requests import twilio_api, make_request

#returning users latitude and longitude
def get_user_lat_long_api(stringToSend):
    sourceOfCall = {"sourceOfCall": "locationiq"}
    paramsData = {"paramsData": "params"}
    getPost = {"getPost": "get"}
    apiUrl = {"apiUrl": API_URLS['locationiq_v1']}
    apiEndpoint = {"apiEndpoint": "search.php"}
    params =  {"params":{'key': locationiqTokenKey,
        'q': stringToSend,
        'format': 'json'}}
    result = make_request(**apiUrl, **apiEndpoint, **paramsData, **getPost, **params, **sourceOfCall)

    # depreciated due to make_requests
    # result = make_request_params(**apiUrl, **apiEndpoint, **params)

    try:
        userLat = result[0]["lat"]
        userLon = result[0]["lon"]
        return "success", userLat, userLon
    except:
        return "Can not retrieve latitude and longitude for this place...","",""

def get_user_weather_forecast_api(**kwargs):
    """

    :param kwargs:
    :return:
    """
    try:
        userLen = kwargs["userLat"]
        userLong = kwargs["userLong"]
        params = kwargs["params"]
    except:
        return "error"
    make_request_parameters = {
        "apiUrl": API_URLS['darksky_forecast'].format(darkSkyToken, userLen, userLong),
        "sourceOfCall": "darksky",
        "paramsData": "params",
        "getPost": "get",
        "params": params
    }
    result = make_request(**make_request_parameters)
    #TODO add requst status code
    # depreciated due to make_requests

    return result

def send_sms_message_api(userMobileNumber, processedForecastMessage):
    twilio_api(userMobileNumber, processedForecastMessage, twilioAccountSid, twilioAuthToken, myTwilioTelephone)

def get_recaptcha_api(recaptcha_response):
    ''' Begin reCAPTCHA validation '''

    make_request_parameters = {
        "sourceOfCall": "rechaptcha",
        "apiUrl": API_URLS['google_recaptcha'],
        "paramsData": "data",
        "getPost": "post",
        "data": {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
    }
    result = make_request(**make_request_parameters)
    return result
    ''' End reCAPTCHA validation '''
