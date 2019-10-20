
from django.shortcuts import render
from mobile_phone.models import user_phone

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]

    #Dashboard default values are false.
    hasCityCountry = False
    hasCityCountryMessage = "City and Country are required fields for weather forecast"
    hasCityCountryStatusColor = "Red"
   
    hasAddress = False
    hasAddressMessage = "Address is required to receive a more precise forecast"
    hasAddressStatusColor = "yellow"

    hasMobileNumber = False
    hasMobileNumberMessage = "Your account has no mobile number"
    hasMobileNumberStatusColor = "red"

    isForecastTimeSet = False
    isForecastTimeSetMessage = "Forecast time is not set"
    isForecastTimeSetStatusColor = "red"

    isMobileValidated = False
    isMobileValidatedMessage = "Your mobile phone is not validated"
    isMobileValidatedStatusColor = "red"

    wantsToReceiveWeatherSMS = False
    wantsToReceiveWeatherSMSMessage = "To receive messages select that inside your mobile configuration"
    wantsToReceiveWeatherSMSStatusColor = "red"    

    if (user1.userCity is not None and (len(user1.userCountry.name)>1) ):
        hasCityCountry = True
        hasCityCountryMessage = "City and Country are inputed"
        hasCityCountryStatusColor = "Green"


    if user1.userAddress is not None:
        hasAddress = True
        hasAddressMessage = "Address is inputed"
        hasAddressStatusColor = "green"

   #Check mobile number, forecast time etc only if instance of user_phone object exist
    try:
        found_u_p_data = user_phone.objects.get(userMobilePhone=user1)
        if found_u_p_data.phoneNumber is not None and len(found_u_p_data.phoneNumber) != 0:
            hasMobileNumber = True
            hasMobileNumberMessage = "You have inputed a mobile number"
            hasMobileNumberStatusColor = "green"

        if ((found_u_p_data.timeWeatherSMS is not None) and (found_u_p_data.timeWeatherSMS is not "")):
            isForecastTimeSet = True
            isForecastTimeSetMessage = "Forecast time is set"
            isForecastTimeSetStatusColor = "green"

        isMobileValidated = found_u_p_data.isMobileValidated 
        if isMobileValidated:
            isMobileValidatedMessage = "your mobile phone has been validated"
            isMobileValidatedStatusColor = "green"
       
        wantsToReceiveWeatherSMS = found_u_p_data.wantsToReceiveWeatherSMS 
        if wantsToReceiveWeatherSMS:
            wantsToReceiveWeatherSMSMessage = "You have selected to receive forecast text messages"
            wantsToReceiveWeatherSMSStatusColor = "green"
       

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
        isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor \