#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone
from .dashboard_status_processing import dashboard_status_processing
from .choice import INDEX_PAGE_CITIES
from api_relay.views import get_user_weather_forecast_api
from weather.tasks import get_default_cities_forecast_dark_sky


def index_status_processing():
   resultForecastRaw = []
   result = {}
   for x in INDEX_PAGE_CITIES:
      for k, v in x.items():
         city = k
         lat = v["lat"]
         lon = v["lon"]

         #params =  {"params1":{'units': "auto","exclude":"minutely,hourly,daily,alerts,flags"}}
         data =  {'userLat': lat,"userLong": lon, "params":{'units': "si","exclude":"minutely,hourly,daily,alerts,flags"}}           
         asyncForecast = get_default_cities_forecast_dark_sky.delay(**data)
         resultForecastRaw.append(asyncForecast)   

  
   for x in range(0, len(INDEX_PAGE_CITIES)):
     # print(INDEX_PAGE_CITIES[x])
      for key in INDEX_PAGE_CITIES[x]:
         resultForecast = resultForecastRaw[x].get()
       #  print(resultForecast)
         temperature = resultForecast["currently"]["temperature"]
         result[key] = temperature
         #print(str(test[x].get()))
      #print("forecast for " + k + ": " + str(resultForecast))
   print(result)
   return result


def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      result = index_status_processing()
      return render(request,'index.html',
      {
         'result':result
      }
      
      
      )

def dashboard(request):
   if request.user.is_authenticated:
      

      user1 = {"user1": request.user} 
      
      dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor, \
      hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
      hasAddress,hasAddressMessage, hasAddressStatusColor, \
      isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
      wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
      isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor \
         = dashboard_status_processing(**user1)
      
    
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
         'isForecastTimeSetStatusColor': isForecastTimeSetStatusColor
         })


   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




