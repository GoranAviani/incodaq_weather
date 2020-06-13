#Location of non app single pages
from django.shortcuts import render, redirect
from .dashboard_status_processing import dashboard_status_processing
from weather.tasks import get_periodic_forecast_for_default_cities
from weather.models import default_cities
from weather.forms import SearchBarForm
from weather.views import process_forecast_api_message
from django.http import HttpResponse
from api_relay.views import get_user_lat_long_api, get_user_weather_forecast_api, get_recaptcha_api
from incodaq_weather.constants import INDEX_CITIES_DEFAULT_VALUES
import logging


def get_default_cities_temp():
   result = []
   foundDefaultCitiesQuerySet = default_cities.objects.all()
   if not foundDefaultCitiesQuerySet:
       return INDEX_CITIES_DEFAULT_VALUES
   else:
      for x in foundDefaultCitiesQuerySet:
         # {'city': city, 'temp': processedTemp, 'iconDesc': processedIconText}
         result.append({'city': x.city, 'temp': x.temperature, 'iconDesc': x.weatherIconDesc})
      return result

def processing_forecast_search_bar_form(request):
    form = SearchBarForm(request.POST)
    if form.is_valid():
        # if user not auth do rechaptcha
        if not request.user.is_authenticated:
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            result = get_recaptcha_api(recaptcha_response)

            if not result['success']:
                customErrorMessage = "Invalid reCAPTCHA. Please try again."
                customErrorMessageColor = "red"
                return "failure", 'full_forecast.html', customErrorMessage, customErrorMessageColor
            ''' end reCAPTCHA validation '''

        cd = form.cleaned_data
        a = cd.get('searchBarInput')  # get the user input data
        latLogAPIStatus, userLat, userLon = get_user_lat_long_api(a)
        if latLogAPIStatus != 'success':
            # Current failure message = "Can not retrieve latitude and longitude for this place..."
            return "failure", "full_forecast.html", latLogAPIStatus, "red"
        else:
            try:
                data = {'userLat': userLat, "userLong": userLon, "params": {'units': "auto"}}
                weatherForecast = get_user_weather_forecast_api(**data)
                if weatherForecast == "error":  # get_user_weather returns only error or message
                    logging.getLogger("darksky_error_logger").error("Dark Sky ERROR response: %s", weatherForecast)
                    customErrorMessage = "Error while fetching you forecast, please contact our support."
                    customErrorMessageColor = "red"
                    return "failure", 'full_forecast.html', customErrorMessage, customErrorMessageColor
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
                        return "failure", "full_forecast.html", customErrorMessage, customErrorMessageColor
            except:
                logging.getLogger("darksky_error_logger").error(
                    "Something went wrong with try except in view function processing_forecast_search_bar_form")
                return "failure", "full_forecast.html", "Something went wrong trying to get your forecast", "red"

    else:
        #Form was not successfully validated
        isValidFormErrorMessages = form.errors
        messageColor = "red"
        return "failure", "full_forecast.html", isValidFormErrorMessages, messageColor

def index(request):
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
       if request.method == 'POST':
           status, htmlPage, customMessage, customMessageColor = processing_forecast_search_bar_form(request)
           if status == "failure":
               return render(request, htmlPage,
                             {
                                 'customErrorMessage': customMessage,
                                 'customErrorMessageColor': customMessageColor})
           elif status == "success":
                return render(request, htmlPage,
                         {
                             'processedForecastMsg': customMessage}) #No color needed for processedForecastMsh
           else:
               return render(request, "full_forecast.html",
                             {
                                 'customErrorMessage': "Unknown status returned from processing_forecast_search_bar_form to index page.",
                                 'customErrorMessageColor': "red"})
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
          status, htmlPage, customMessage, customMessageColor = processing_forecast_search_bar_form(request)
          if status == "failure":
              return render(request, htmlPage,
                            {
                                'customErrorMessage': customMessage,
                                'customErrorMessageColor': customMessageColor})
          elif status == "success":
              return render(request, htmlPage,
                            {
                                'processedForecastMsg': customMessage})  #No color needed for processedForecastMsg
          else:
              return render(request, "full_forecast.html",
                            {
                                'customErrorMessage': "Unknown status returned from processing_forecast_search_bar_form to dashboard page.",
                                'customErrorMessageColor': "red"})
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




