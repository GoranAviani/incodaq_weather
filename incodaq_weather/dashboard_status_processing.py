
from django.shortcuts import render
from mobile_phone.models import user_phone

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]


    if (user1.userCity is not None and (len(user1.userCountry.name)>1) ):
        hasCityCountry = True
        hasCityCountryMessage = "All is ok here"
        hasCityCountryStatusColor = "Green"
    else:
        hasCityCountry = False
        hasCityCountryMessage = "City and Country are required fields for weather forecast"
        hasCityCountryStatusColor = "Red"

    if user1.userAddress is not None:
        hasAddress = True
    else:
        hasAddress = False
   
    try:
        found_u_p_data = user_phone.objects.get(userMobilePhone=user1)
        if found_u_p_data.phoneNumber is not None:
            hasMobileNumber = True
        else:
            hasMobileNumber = False
        isMobileValidated = found_u_p_data.isMobileValidated 
        wantsToReceiveWeatherSMS = found_u_p_data.wantsToReceiveWeatherSMS 

        if ((found_u_p_data.timeWeatherSMS is not None) and (found_u_p_data.timeWeatherSMS is not "")):
            isForecastTimeSet = True
        else:
            isForecastTimeSet = False

    except:
        hasMobileNumber = False
        isMobileValidated = False
        wantsToReceiveWeatherSMS = False
        isForecastTimeSet = False
        
       
    return hasMobileNumber, hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, hasAddress, isMobileValidated, wantsToReceiveWeatherSMS, isForecastTimeSet