
from django.shortcuts import render
from mobile_phone.models import user_phone
from incodaq_weather.constants import green_string, red_string, yellow_string

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]

    #Dashboard default values are false.
    hasCityCountry = False
    hasCityCountryMessage = "City and Country are required fields for weather forecast"
    hasCityCountryStatusColor = red_string
   
    hasAddress = False
    hasAddressMessage = "Address is required to receive a more precise forecast"
    hasAddressStatusColor = yellow_string

    hasMobileNumber = False
    hasMobileNumberMessage = "Your account has no mobile number"
    hasMobileNumberStatusColor = red_string

    isForecastTimeSet = False
    isForecastTimeSetMessage = "Forecast time is not set"
    isForecastTimeSetStatusColor = red_string

    isMobileValidated = False
    isMobileValidatedMessage = "Your mobile phone is not validated"
    isMobileValidatedStatusColor = red_string

    wantsToReceiveWeatherSMS = False
    wantsToReceiveWeatherSMSMessage = "To receive messages select that inside your mobile configuration"
    wantsToReceiveWeatherSMSStatusColor = red_string

    if (user1.userCity is not None and (len(user1.userCountry.name)>1) ):
        hasCityCountry = True
        hasCityCountryMessage = "City and Country are inputed"
        hasCityCountryStatusColor = green_string


    if user1.userAddress is not None:
        hasAddress = True
        hasAddressMessage = "Address is inputed"
        hasAddressStatusColor = green_string

   #Check mobile number, forecast time etc only if instance of user_phone object exist
    try:
        found_u_p_data = user_phone.objects.get(userMobilePhone=user1)
        if found_u_p_data.phoneNumber is not None and len(found_u_p_data.phoneNumber) != 0:
            hasMobileNumber = True
            hasMobileNumberMessage = "You have inputed a mobile number"
            hasMobileNumberStatusColor = green_string

        if ((found_u_p_data.timeWeatherSMS is not None) and (found_u_p_data.timeWeatherSMS is not "")):
            isForecastTimeSet = True
            isForecastTimeSetMessage = "Forecast time is set"
            isForecastTimeSetStatusColor = green_string

        isMobileValidated = found_u_p_data.isMobileValidated 
        if isMobileValidated:
            isMobileValidatedMessage = "your mobile phone has been validated"
            isMobileValidatedStatusColor = green_string
       
        wantsToReceiveWeatherSMS = found_u_p_data.wantsToReceiveWeatherSMS 
        if wantsToReceiveWeatherSMS:
            wantsToReceiveWeatherSMSMessage = "You have selected to receive forecast text messages"
            wantsToReceiveWeatherSMSStatusColor = green_string
       

    except:
        #model instances are still not created therefore default values (set as false in the 
        # begginig of this function) will apply
        pass
        
    #Display custom dashboard message if there is any       
    try:
        dashboardStatusMessage = kwargs["dashboardStatus"]
        dashboardStatusColor = kwargs["statusColor"]
    except:
        dashboardStatusMessage = "Hello and welcome to your dashboard."
        dashboardStatusColor = "green"


    return dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor,\
        hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
        hasAddress, hasAddressMessage, hasAddressStatusColor, \
        isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
        wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
        isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor