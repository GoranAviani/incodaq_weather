#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone
from .dashboard_status_processing import dashboard_status_processing
from .choice import INDEX_PAGE_CITIES
from weather.tasks import get_periodic_forecast_for_default_cities

def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      get_periodic_forecast_for_default_cities()
      return render(request,'index.html')

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




