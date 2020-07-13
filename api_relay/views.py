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

#This is the place where api functions are getting called from

from .making_requests import twilio_api, make_request

def get_user_lat_long_api(stringToSend):
    """
    returning users latitude and longitude

    :param stringToSend:
    :return:
    """
    make_request_parameters = {
        "sourceOfCall": "locationiq",
        "paramsData": "params",
        "getPost": "get",
        "apiUrl": API_URLS['locationiq_v1'],
        "params": {'key': locationiqTokenKey,
                   'q': stringToSend,
                   'format': 'json'}
    }
    result = make_request(**make_request_parameters)

    try:
        userLat = result[0]["lat"]
        userLon = result[0]["lon"]
        return "success", userLat, userLon
    except:
        return "Can not retrieve latitude and longitude for this place...", "", ""

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
