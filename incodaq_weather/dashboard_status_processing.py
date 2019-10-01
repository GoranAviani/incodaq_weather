
from django.shortcuts import render
from mobile_phone.models import user_phone

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]

    if (user1.userCity is not None and (len(user1.userCountry.name)>1) ):
        hasCityCountry = True
        hasCityCountryMessage = "City and Country are inputed"
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
        if found_u_p_data.phoneNumber is not None and len(found_u_p_data.phoneNumber) != 0:
            hasMobileNumber = True
            hasMobileNumberMessage = "You have inputed a mobile number"
            hasMobileNumberStatusColor = "green"
            

        else:
            hasMobileNumber = False
            hasMobileNumberMessage = "Your account has no mobile number"
            hasMobileNumberStatusColor = "red"
        if ((found_u_p_data.timeWeatherSMS is not None) and (found_u_p_data.timeWeatherSMS is not "")):
            isForecastTimeSet = True
        else:
            isForecastTimeSet = False

        isMobileValidated = found_u_p_data.isMobileValidated 
        if isMobileValidated:
            isMobileValidatedMessage = "your mobile phone has been validated"
            isMobileValidatedStatusColor = "green"
        else:
            isMobileValidatedMessage = "Your mobile phone is not validated"
            isMobileValidatedStatusColor = "red"

        wantsToReceiveWeatherSMS = found_u_p_data.wantsToReceiveWeatherSMS 
            


    except:
        hasMobileNumber = False
        hasMobileNumberMessage = "Something went wrong and we can not see if you have a phone number"
        hasMobileNumberStatusColor = "red"
        isMobileValidated = False
        isMobileValidatedMessage ="Someting went wrong and we cant confirm if the phone number is validated" 
        isMobileValidatedStatusColor = "red"
        wantsToReceiveWeatherSMS = False
        isForecastTimeSet = False
        
       
    return hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor,\
        hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
            hasAddress, \
            isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
                wantsToReceiveWeatherSMS, isForecastTimeSet \