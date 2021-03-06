from django.shortcuts import render

# Create your views here.

from expanded_user.models import custom_user
from django.http import HttpResponse
from mobile_phone.models import user_phone
from api_relay.views import get_user_lat_long_api, get_user_weather_forecast_api, send_sms_message_api
import time
import datetime
from incodaq_weather.processing import *

from .tasks import *
from .forms import SearchBarForm

# Create your views here.

def check_if_time_to_send_sms(userForecastTimeList, userTimeZone):
    # if time not to send sms return "DontSendSMS"
    # if time to send sms has passed by 29 minutes then send the sms (assuming it takes 29 minutes ti send all sms)
    # if it didnt pass then it is now or will be sent in the next cronjon (every 30 minutes cron job runs)
    nowTime = datetime.datetime.now()
    nowHours = nowTime.hour
    nowMinutes = nowTime.minute
    userHours = int(userForecastTimeList[0]) - int(userTimeZone)
    userMinutes = int(userForecastTimeList[1])

    if (userHours == nowHours):
        pass
    else:
        return "DontSendSMS"

    # if the time is ecaxt
    if (userMinutes == nowMinutes):
        return "sendSMSNow"
    elif (userMinutes in range(nowMinutes - 29, nowMinutes)):
        # if the time has passed in the last 29 min
        # but obviously was not run in the last vron job (would be -30 min then)
        return "sendSMSNow"
    else:
        return "DontSendSMS"


def check_user_weather_SMS_time_format(usersWeatherSMSTimeList):
    # check if [0] us between 0 and 24 and if [1] is 0 or 30, if inside
    # these parameters it is ok, if not the time is wrong
    # if format bad please return "error"
    try:
        areBothDigits = ((usersWeatherSMSTimeList[0].isdigit()) and (usersWeatherSMSTimeList[1].isdigit()))
    except:
        return "error", usersWeatherSMSTimeList

    try:
        isHour0to24 = ((int(usersWeatherSMSTimeList[0]) >= 0) and (int(usersWeatherSMSTimeList[0]) < 25))
    except:
        return "error", usersWeatherSMSTimeList

    try:
        isMinute0to60 = ((int(usersWeatherSMSTimeList[1]) == 0) or (int(usersWeatherSMSTimeList[1]) == 30))
    except:
        return "error", usersWeatherSMSTimeList

    return "sendSMS", usersWeatherSMSTimeList


def check_user_forecast_time(user_phone_instance, user):
    usersWeatherSMSTime = user_phone_instance.timeWeatherSMS
    userTimeZone = user.userTimeZone
    charForSplit = ":"  # time hours and minutes are splitted by :
    status, usersWeatherSMSTimeList = split_by_char(usersWeatherSMSTime, charForSplit)
    if status == "error":
        return "DontSendSMS", "Forecast time is in wrong format."
    # status, usersWeatherSMSTimeList = check_user_weather_SMS_time_format(usersWeatherSMSTimeList)
    # if status != "error":
    status = check_if_time_to_send_sms(usersWeatherSMSTimeList, userTimeZone)
    if status == "DontSendSMS":
        return "DontSendSMS", "Time set for weather forecast is not now."
    # else:
    #    return "DontSendSMS", "Forecast time is in wrong time/number format."
    # else:
    #   return "DontSendSMS", "Forecast time is in wrong format."

    return "sendSMS", "Weater forecast time is OK."


def get_mobile_phone(user_phone_instance):
    if (user_phone_instance.isMobileValidated == True and user_phone_instance.wantsToReceiveWeatherSMS == True):
        # print(user_phone_instance)
        if (user_phone_instance.phoneCountryCode != None and user_phone_instance.phoneCountryCode != None):
            phoneCountryCode = user_phone_instance.phoneCountryCode
            phoneNumber = user_phone_instance.phoneNumber

            status = "OK"
            result = phoneCountryCode + phoneNumber
            statusMessage = "Mobile phone check is OK."
            return status, statusMessage, result
        else:
            status = "DontSendSMS"
            result = ""
            statusMessage = "Mobile phone is not in right format."
            return status, statusMessage, result
    else:
        status = "DontSendSMS"
        result = ""
        statusMessage = "Mobile phone needs to be validated and approved by user to receive weather forecast text messages."
        return status, statusMessage, result


def process_forecast_api_message(**kwargs):
    """
    This function caters for weather processing for different stakeholders:
    text message,
    default index cities with basic forceast,
    default index cities with advanced forecast,
    index/dashboard searsh bar forecast

    :param kwargs:
    :return:
    """
    typeOfCall = kwargs["typeOfCall"]

    if typeOfCall == "sms_message":
        apiResponse = kwargs["apiResponse"]
        forecastLocation = kwargs["forecastLocation"]
        current_temperature = str(round(apiResponse["currently"]["temperature"]))
        daily_temp_lowest = str(round(apiResponse["daily"]["data"][0]["temperatureLow"]))
        daily_temp_highest = str(round(apiResponse["daily"]["data"][0]["temperatureHigh"]))
        current_summary = apiResponse["currently"]["summary"]
        daily_summary = apiResponse["hourly"]["summary"]

        processedMessage = ("Forecast for {}: Now: {}C and {}. Low: {}C, High: {}C. {} Incodaq Weather"
            .format(
            forecastLocation,
            current_temperature,
            current_summary,
            daily_temp_lowest,
            daily_temp_highest,
            daily_summary))

        return "success", processedMessage
    elif typeOfCall == "default_cities_basic_forecast":
        apiResponse = kwargs["apiResponse"]
        result = apiResponse["currently"]["temperature"]
        return "success", result
    elif typeOfCall == "default_cities_adv_forecast":
        apiResponse = kwargs["apiResponse"]
        temperature = apiResponse["currently"]["temperature"]
        iconDesc = apiResponse["currently"]["icon"]
        return "success", temperature, iconDesc
    elif typeOfCall == "search_bar_forecast":
        apiResponse = kwargs["apiResponse"]
        forecastLocation = kwargs["forecastLocation"]
        currentlyIcon = apiResponse["currently"]["icon"]
        hourlyIcon = apiResponse["hourly"]["icon"]

        processedMessage = {
        "currentlyTemp": str(round(apiResponse["currently"]["temperature"]))
        , "dailyLow": str(round(apiResponse["daily"]["data"][0]["temperatureLow"]))
        ,"dailyHigh": str(round(apiResponse["daily"]["data"][0]["temperatureHigh"]))
        ,"currentlySummary": str(apiResponse["currently"]["summary"])
        ,"hourlySummary": str(apiResponse["hourly"]["summary"])
        , "currentlyUV": str(apiResponse["currently"]["uvIndex"])
        , "currentlyIcon": currentlyIcon
        , "hourlyIcon": hourlyIcon
        ,"forecastLocation": forecastLocation
        }

        return "success", processedMessage
    else:
        return "error", ""


def get_user_mobile_and_check_time(user, typeOfRequest):
    """
    # This function witll return user mobile if user is approved and
    # wants to receive weather forecast
    :param user:
    :param typeOfRequest:
    :return:
    """
    try:
        user_phone_instance = user_phone.objects.get(userMobilePhone=user)
    except:
        # user does not have anything in user phone model
        status = "DontSendSMS"
        resultMobileNumber = ""
        statusMessage = "No user phone instance"
        return status, statusMessage, resultMobileNumber

    # check do we send sms now or not now
    # If it is a manual request for weather prognosis (done by user), there is no need to check the time
    if typeOfRequest == "manualWeatherRequest":
        status = "SendSMS"
        statusMessageWeather = "Mobile Phone approved. Forecast time check is skipped for manual weather request."
    else:
        status, statusMessageWeather = check_user_forecast_time(user_phone_instance, user)

    if status != "DontSendSMS":
        status, statusMessageMobile, resuresultMobileNumber = get_mobile_phone(user_phone_instance)
        return status, (statusMessageWeather + " " + statusMessageMobile), resuresultMobileNumber

    status = "DontSendSMS"
    resuresultMobileNumber = ""
    # statusMessage = "Forecast time for this user is not now or is in wrong format. "
    return status, statusMessageWeather, resuresultMobileNumber


def get_string_for_forecast(userAddress, userCity, userCountry):
    stringToSend = ""
    if ((userCity != None) and (len(userCity) > 1) and (len(userCountry) > 1)):
        if ((userAddress != None) and (len(userAddress) > 1)):
            return str(userAddress) + "," + str(userCity) + "," + str(userCountry)
        else:
            return str(userCity) + "," + str(userCountry)
    else:
        return "failure"

    return stringToSend


# the actual sending of the forecast
def send_daily_forecast(user, typeOfRequest):
    userCity = user.userCity
    userLat = user.userLatitude
    userLong = user.userLongitude

    #fetc user lat lon if they are missing
    if ((userLat != None and userLat != "") and (userLong != None and userLong != "")):
        userMobileStatus, statusMessage, userMobileNumber = get_user_mobile_and_check_time(user, typeOfRequest)
        # if userForecastTimeList not "now" or in the last 2 hours (processig time was long)
        # then dont send because its still not the time do send sms
        # else the time is now so please send sms to user

        if userMobileStatus == "DontSendSMS":
            return statusMessage  # user mobile is not approved /does not want to receive sms
        else:
            # all user checks have passed and he is to receive his forecast sms
            # return weather forecast for his lat and long
            try:
                data = {'userLat': userLat, "userLong": userLong, "params": {'units': "auto"}}
                weatherForecast = get_user_weather_forecast_api(**data)
                if weatherForecast == "error":
                    return "Something went wrong with getting the weather forecast. Plese contact support."
            except:
                return "Something went wrong with getting the data needed for the weather forecast. Plese contact support."

            # Process raw api data to text about a forecast
            data = {'typeOfCall': "sms_message", "forecastLocation": userCity, "apiResponse": weatherForecast}
            processedForecastMsgStatus, processedForecastMsg = process_forecast_api_message(**data)
            # print(processedForecastMessage)

            # delay of 0.5s because free Twilio account supports 2 messages in a second.
            # if number is greather than that 2 twilio will return 429 code.
            time.sleep(0.5)

            # send sms message only if processedForecastMsgStatus is a success
            if processedForecastMsgStatus == "success":
                try:
                    send_sms_message_api(userMobileNumber, processedForecastMsg)
                    return statusMessage
                except:
                    return "Something went wrong with sending the SMS messages. Please contact support."
            else:
                return "Something went wrong with preparing the SMS messages. Please contact support."
    else:
        return "To use the weather forecast feature the user needs to have a minimum of a city and country saved in the user profile."


# This function will send weather sms message to all users that have address and city
# and have been approved and want to receive sms messages
def send_daily_forecast_to_all(request):
    # users = custom_user.objects.all()
    # typeOfRequest = "autoWeatherRequest"
    # for user in users:
    # weather.send_task('incodaq_weather.tasks.send_daily_forecast_celery', args=(user, 'two'))
    # send_daily_forecast_celery(user, typeOfRequest)

    send_daily_forecast_to_all_celery()

    # statusMessage = send_daily_forecast(user, typeOfRequest)
    # status message is not really used for now but can be used to print a list
    # of users and who got sms and who not with a reason why not
    statusMessage = 'Daily forecast has been sent to all users.'
    return render(request, 'weather/manual_forecast_status.html',
                  {'statusMessage': statusMessage})


def send_daily_forecast_to_user(request):
    user = request.user
    typeOfRequest = "manualWeatherRequest"
    statusMessage = send_daily_forecast(user, typeOfRequest)
    return render(request, 'weather/manual_forecast_status.html',
                  {'statusMessage': statusMessage, 'username': user.username})