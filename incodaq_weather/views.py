#Location of non app single pages
from django.shortcuts import render, redirect
from .dashboard_status_processing import dashboard_status_processing
from weather.tasks import get_periodic_forecast_for_default_cities
from weather.models import default_cities
from weather.forms import SearchBarForm


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
         form = SearchBarForm(request.POST)
         if form.is_valid():
            cd = form.cleaned_data
            a = cd.get('searchBarInput')
   #TODO
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




