
from django.shortcuts import render
from mobile_phone.models import user_phone
from incodaq_weather.constants import \
    (
    GREEN_STRING,
    RED_STRING,
    YELLOW_STRING,
    CITY_COUNTRY_NEGATIVE_STATUS,
    ADDRESS_NEGATIVE_STATUS,
    MOBILE_NUMBER_NEGATIVE_STATUS,
    FORECAST_TIME_NEGATIVE_STATUS,
    MOBILE_NUMBER_VALIDATED_NEGATIVE_STATUS,



)

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]

    #Dashboard default values are false.
    hasCityCountry = False
    hasCityCountryMessage = CITY_COUNTRY_NEGATIVE_STATUS
    hasCityCountryStatusColor = RED_STRING
   
    hasAddress = False
    hasAddressMessage = ADDRESS_NEGATIVE_STATUS
    hasAddressStatusColor = YELLOW_STRING

    hasMobileNumber = False
    hasMobileNumberMessage = MOBILE_NUMBER_NEGATIVE_STATUS
    hasMobileNumberStatusColor = RED_STRING

    isForecastTimeSet = False
    isForecastTimeSetMessage = FORECAST_TIME_NEGATIVE_STATUS
    isForecastTimeSetStatusColor = RED_STRING

    isMobileValidated = False
    isMobileValidatedMessage = MOBILE_NUMBER_VALIDATED_NEGATIVE_STATUS
    isMobileValidatedStatusColor = RED_STRING

    wantsToReceiveWeatherSMS = False
    wantsToReceiveWeatherSMSMessage = "To receive messages select that inside your mobile configuration"
    wantsToReceiveWeatherSMSStatusColor = RED_STRING

    if (user1.userCity is not None and (len(user1.userCountry.name)>1) ):
        hasCityCountry = True
        hasCityCountryMessage = "City and Country are inputed"
        hasCityCountryStatusColor = GREEN_STRING


    if user1.userAddress is not None:
        hasAddress = True
        hasAddressMessage = "Address is inputed"
        hasAddressStatusColor = GREEN_STRING

   #Check mobile number, forecast time etc only if instance of user_phone object exist
    try:
        found_u_p_data = user_phone.objects.get(userMobilePhone=user1)
        if found_u_p_data.phoneNumber is not None and len(found_u_p_data.phoneNumber) != 0:
            hasMobileNumber = True
            hasMobileNumberMessage = "You have inputed a mobile number"
            hasMobileNumberStatusColor = GREEN_STRING

        if ((found_u_p_data.timeWeatherSMS is not None) and (found_u_p_data.timeWeatherSMS is not "")):
            isForecastTimeSet = True
            isForecastTimeSetMessage = "Forecast time is set"
            isForecastTimeSetStatusColor = GREEN_STRING

        isMobileValidated = found_u_p_data.isMobileValidated 
        if isMobileValidated:
            isMobileValidatedMessage = "your mobile phone has been validated"
            isMobileValidatedStatusColor = GREEN_STRING
       
        wantsToReceiveWeatherSMS = found_u_p_data.wantsToReceiveWeatherSMS 
        if wantsToReceiveWeatherSMS:
            wantsToReceiveWeatherSMSMessage = "You have selected to receive forecast text messages"
            wantsToReceiveWeatherSMSStatusColor = GREEN_STRING
       

    except:
        #model instances are still not created therefore default values (set as false in the 
        # begginig of this function) will apply
        pass
        
    #Display custom dashboard message if there is any       
    try:
        dashboardStatusMessage = kwargs["dashboardStatus"]
        dashboardStatusColor = kwargs["statusColor"]
    except:
        dashboardStatusMessage = "Welcome to your dashboard"
        dashboardStatusColor = GREEN_STRING


    return dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor,\
        hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
        hasAddress, hasAddressMessage, hasAddressStatusColor, \
        isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
        wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
        isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor