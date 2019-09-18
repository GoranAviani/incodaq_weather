from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse

def dashboard_status_processing(**kwargs):
 
    user1 = kwargs["user1"]


    if (user1.userCity is not None and user1.userCountry is not None):
        hasCityCountry = True
    else:
        hasCityCountry = False
   
    if user1.userAddress is not None:
        hasAddress = True
    else:
        hasAddress = False
   
    try:
        found_u_p_data = user_phone.objects.get(userMobilePhone=request.user) 
        hasMobileNumber = True
        isMobileValidated = True
        wantsToReceiveWeatherSMS = True
    except:
        hasMobileNumber = False
        isMobileValidated = False
        wantsToReceiveWeatherSMS = False
        
       
    return hasMobileNumber, hasCityCountry, hasAddress, isMobileValidated, wantsToReceiveWeatherSMS