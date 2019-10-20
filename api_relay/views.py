from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from incodaq_weather.local_settings import locationiqTokenKey, darkSkyToken, twilioAccountSid, twilioAuthToken, myTwilioTelephone


# Create your views here.
#This is the place where api functions are getting called from

from .making_requests import make_request_params, twilio_api

#returning users latitude and longitude
def get_user_lat_long_api(stringToSend):
    apiUrl = {"apiUrl": "https://eu1.locationiq.com/v1/"}
    apiEndpoint = {"apiEndpoint": "search.php"}
    params =  {"params1":{'key': locationiqTokenKey,
        'q': stringToSend,
        'format': 'json'}}
    result = make_request_params(**apiUrl, **apiEndpoint, **params)
    
    try:
        userLat = result[0]["lat"]
        userLon = result[0]["lon"]
        return "success", userLat, userLon
    except:
        return "failure","",""

def get_user_weather_forecast_api(userLen, userLong):
    apiUrl = {"apiUrl": "https://api.darksky.net/forecast/"}
    apiEndpoint = {"apiEndpoint": darkSkyToken + "/" + userLen +","+userLong}
    params =  {"params1":{'units': "auto",}}
    result = make_request_params(**apiUrl, **apiEndpoint, **params)
    #print(result)    
    return result

def send_sms_message_api(userMobileNumber, processedForecastMessage):
    twilio_api(userMobileNumber, processedForecastMessage, twilioAccountSid, twilioAuthToken, myTwilioTelephone)