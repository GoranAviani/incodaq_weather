#Location of non app single pages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mobile_phone.models import user_phone
from mobile_phone.models import user_phone

def index(request):
#   return render(request,'index.html')
   if request.user.is_authenticated:
      return redirect('dashboard')
   else:
      return render(request,'index.html')

def dashboard(request):
   if request.user.is_authenticated:
      

  
      #Choices are: date_joined, email, first_name, groups, id, is_active, is_staff, 
      # is_superuser, last_login, last_name, logentry, password, userAddress, userCity, 
      # userCountry, userMobileNumber, user_permissions, user_phone, username
      user1 = request.user
      ###user = user_phone.objects.get(userMobilePhone=request.user)
      found_u_p_data = user_phone.objects.get(userMobilePhone=request.user) 
     
    
   
      dashboardStatus = "Hi, welcome to your dashboard."
      statusColor = "green"
  
      return render(request, 'dashboard.html', 
      {
      'dashboardStatus':dashboardStatus,
      'statusColor': statusColor,
      #'hasMobileNumber': hasMobileNumber,
      #'hasCityCountry': hasCityCountry,
      #'hasAddress': hasAddress,
      #'isMobileValidated': isMobileValidated,
      #'sendWeatherSMS'
      })


   else:
        #if user is not authenticated inform him of that
        return render(request, 'other_pages/not_authenticaded.html')




