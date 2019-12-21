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

def index(request):
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      defaultCitiesTemp = get_default_cities_temp()
      return render(request, 'index.html',
      {'defaultCitiesTemp': defaultCitiesTemp}
      )

def dashboard(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
      #this is the "forecast search bar" that is called from dashboard
         form = SearchBarForm(request.POST)
         if form.is_valid():
            cd = form.cleaned_data
            a = cd.get('searchBarInput') #get the user input data
            latLogAPIStatus, userLat, userLon = get_user_lat_long_api(a)
            if latLogAPIStatus != 'success':

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
   #TODO - fetch forecast via api and display on another page.
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




