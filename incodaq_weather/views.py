#Location of non app single pages
from django.shortcuts import render, redirect
from .dashboard_status_processing import dashboard_status_processing
from weather.tasks import get_periodic_forecast_for_default_cities
from weather.models import default_cities
from weather.forms import SearchBarForm
from weather.views import process_forecast_api_message
from django.http import HttpResponse
from api_relay.views import get_user_lat_long_api, get_user_weather_forecast_api
import logging
from django.conf import settings
#TODO remove requests when switching api calls to api reay model
import requests

def get_default_cities_temp():
   result = []
   try:
      foundDefaultCitiesQuerySet = default_cities.objects.all()
      for x in foundDefaultCitiesQuerySet:
         # {'city': city, 'temp': processedTemp, 'iconDesc': processedIconText}
         result.append({'city': x.city, 'temp': x.temperature, 'iconDesc': x.weatherIconDesc})
      return result
   except:
      return result

def processing_forecast_search_bar_form(request):
    # if user not auth do rechaptcha

    form = SearchBarForm(request.POST)
    if form.is_valid():
        if not request.user.is_authenticated:

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                pass
                #form.save()
                #messages.success(request, 'New comment added with success!')
            else:
                customErrorMessage = "Invalid reCAPTCHA. Please try again."
                customErrorMessageColor = "red"
                return "customFailure", 'full_forecast.html', customErrorMessage, customErrorMessageColor

        cd = form.cleaned_data
        a = cd.get('searchBarInput')  # get the user input data
        latLogAPIStatus, userLat, userLon = get_user_lat_long_api(a)
        if latLogAPIStatus != 'success':
            # Current failure message = "Can not retrieve latitude and longitude for this place..."
            return "failure", "", latLogAPIStatus, "" #TODO finish sending custom data with message color
        else:
            try:
                data = {'userLat': userLat, "userLong": userLon, "params": {'units': "auto"}}
                weatherForecast = get_user_weather_forecast_api(**data)
                if weatherForecast == "error":  # get_user_weather returns only error or message
                    logging.getLogger("darksky_error_logger").error("Dark Sky ERROR response: %s", weatherForecast)
                    customErrorMessage = "Error while fetching you forecast, please contact our support."
                    customErrorMessageColor = "red"
                    return "customFailure", 'full_forecast.html', customErrorMessage, customErrorMessageColor
                else:
                    # Dark sky forecast api was success now process foreast message
                    data = {'typeOfCall': "search_bar_forecast", "forecastLocation": a,
                            "apiResponse": weatherForecast}
                    processedForecastMsgStatus, processedForecastMsg = process_forecast_api_message(**data)

                    #message processed succesfully + all processes were completed, display search bar forecast
                    if processedForecastMsgStatus == "success":
                        return processedForecastMsgStatus, "full_forecast.html", processedForecastMsg, "green"
                    else:
                        customErrorMessage = "Error while processing the forecast message, please contact our support."
                        customErrorMessageColor = "red"
                        return "customFailure", "full_forecast.html", customErrorMessage, customErrorMessageColor
            except:
                logging.getLogger("darksky_error_logger").error(
                    "Something went wrong with try except in view function processing_forecast_search_bar_form")
                return HttpResponse("Something went wrong with try except in view function processing_forecast_search_bar_form")
                # TODO display this on full_forecast as custom message
    else:
        #Form was not successfully validated
        isValidFormErrorMessages = form.errors
        messageColor = "red"
        return "customFailureNotValid", "full_forecast.html", isValidFormErrorMessages, messageColor

def index(request):
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
       if request.method == 'POST':
           status, htmlPage, customMessage, customMessageColor = processing_forecast_search_bar_form(request)
           if status == "failure":
               return HttpResponse(customMessage)
           elif status == "customFailure":
               return render(request, htmlPage,
                             {
                                 'customErrorMessage': customMessage,
                                 'customErrorMessageColor': customMessageColor})
           elif status == "success":
                return render(request, htmlPage,
                         {
                             'processedForecastMsg': customMessage}) #TODO return color
           elif status == "customFailureNotValid":
               return render(request, htmlPage,
                             {
                                 'isValidFormErrorMessages': customMessage,
                                 'errorMessageColor': customMessageColor})

           else:
               #TODO make custom error message if something else unexpected happends, log it
               pass
       else:
            defaultCitiesTemp = get_default_cities_temp()
            searchBarInputForm = SearchBarForm()
            return render(request, 'index.html',
            {'defaultCitiesTemp': defaultCitiesTemp,
            'searchBarInputForm': searchBarInputForm}
            )

def dashboard(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
          #TODO replace this with processing_forecast_search_bar_form function
      #this is the "forecast search bar" that is called from dashboard
         form = SearchBarForm(request.POST)
         if form.is_valid():
            cd = form.cleaned_data
            a = cd.get('searchBarInput') #get the user input data
            latLogAPIStatus, userLat, userLon = get_user_lat_long_api(a)
            if latLogAPIStatus != 'success':
                #Current failure message = "Can not retrieve latitude and longitude for this place..."
               return HttpResponse(latLogAPIStatus) #TODO return error message on full_forecast in new message
            else:
                try:
                    data = {'userLat': userLat, "userLong": userLon, "params": {'units': "auto"}}
                    weatherForecast = get_user_weather_forecast_api(**data)
                    if weatherForecast == "error": #get_user_weather returns only error or message
                        logging.getLogger("darksky_error_logger").error("Dark Sky ERROR response: %s", weatherForecast)
                        customErrorMessage = "Error while fetching you forecast, please contact our support."
                        customErrorMessageColor = "red"
                        return render(request, 'full_forecast.html',
                                      {
                                         'customErrorMessage': customErrorMessage,
                                         'customErrorMessageColor': customErrorMessageColor})
                    else:
                       #Dark sky forecast api was success
                       #process foreast message
                       # TODO process messgage in a new way and display it on full forecast with proper forecast

                       data = {'typeOfCall': "search_bar_forecast", "forecastLocation": a,
                               "apiResponse": weatherForecast}
                       processedForecastMsgStatus, processedForecastMsg = process_forecast_api_message(**data)


                       # send sms message only if processedForecastMsgStatus is a success
                       if processedForecastMsgStatus == "success":
                          # TODO display processedForecastMsg onfull forecast
                          return render(request, 'full_forecast.html',
                                        {
                                           'processedForecastMsg': processedForecastMsg})
                       else:
                           customErrorMessage = "Error while processing the forecast message, please contact our support."
                           customErrorMessageColor = "red"
                           return render(request, 'full_forecast.html',
                                      {
                                         'customErrorMessage': customErrorMessage,
                                         'customErrorMessageColor': customErrorMessageColor})
                except:
                    logging.getLogger("darksky_error_logger").error("Something went wrong with try except in view dashboard search bar forecast")
                    return HttpResponse("Something went wrong with try except in view dashboard search bar forecast")
                     #TODO display this on full_forecast as custom message


            return HttpResponse(latLogAPIStatus)
         else:
            isValidFormErrorMessages = form.errors
            messageColor = "red"
            return render(request, 'full_forecast.html',
                 {
                    'isValidFormErrorMessages': isValidFormErrorMessages,
                     'errorMessageColor': messageColor})
      else:
         user1 = {"user1": request.user}

         dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor, \
         hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
         hasAddress,hasAddressMessage, hasAddressStatusColor, \
         isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
         wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
         isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor \
            = dashboard_status_processing(**user1)

         searchBarInputForm = SearchBarForm()
         return render(request, 'dashboard.html',
         {
            'dashboardStatus':dashboardStatusMessage,
            'statusColor': dashboardStatusColor,
            'hasMobileNumber': hasMobileNumber,
            'hasMobileNumberMessage': hasMobileNumberMessage,
            'hasMobileNumberStatusColor': hasMobileNumberStatusColor,
            'hasCityCountry': hasCityCountry,
            'hasCityCountryMessage': hasCityCountryMessage,
            'hasCityCountryStatusColor': hasCityCountryStatusColor,
            'hasAddress': hasAddress,
            'hasAddressMessage': hasAddressMessage,
            'hasAddressStatusColor': hasAddressStatusColor,
            'isMobileValidated': isMobileValidated,
            'isMobileValidatedMessage': isMobileValidatedMessage,
            'isMobileValidatedStatusColor': isMobileValidatedStatusColor,

            'wantsToReceiveWeatherSMS': wantsToReceiveWeatherSMS,
            "wantsToReceiveWeatherSMSMessage": wantsToReceiveWeatherSMSMessage,
            "wantsToReceiveWeatherSMSStatusColor": wantsToReceiveWeatherSMSStatusColor,

            'isForecastTimeSet': isForecastTimeSet,
            'isForecastTimeSetMessage': isForecastTimeSetMessage,
            'isForecastTimeSetStatusColor': isForecastTimeSetStatusColor,
            'searchBarInputForm': searchBarInputForm

            })


   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




