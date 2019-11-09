#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone
from .dashboard_status_processing import dashboard_status_processing

def index_status_processing():
   return "18", "sunny"


def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      StockholmTemperature, StokcholmWeather = index_status_processing()
      print(StockholmTemperature)
      return render(request,'index.html',
      {
         'StockholmTemperature':StockholmTemperature,
         'StokcholmWeather': StokcholmWeather
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




