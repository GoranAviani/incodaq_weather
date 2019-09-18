#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone
from .dashboard_status_processing import dashboard_status_processing

def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      return render(request,'index.html')

def dashboard(request):
   if request.user.is_authenticated:
      

      user1 = {"user1": request.user}
      hasMobileNumber, hasCityCountry, hasAddress, isMobileValidated, wantsToReceiveWeatherSMS = dashboard_status_processing(**user1)
      
    
   
      dashboardStatus = "Hi there " + request.user.username +", welcome to your dashboard."
      statusColor = "green"
  
      return render(request, 'dashboard.html', 
      {
      'dashboardStatus':dashboardStatus,
      'statusColor': statusColor,
      'hasMobileNumber': hasMobileNumber,
      'hasCityCountry': hasCityCountry,
      'hasAddress': hasAddress,
      'isMobileValidated': isMobileValidated,
      'wantsToReceiveWeatherSMS': wantsToReceiveWeatherSMS
      })


   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




