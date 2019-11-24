from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from .forms import (
    user_signup_form,
    user_profile_form,
    
)

from django.contrib.auth import (
    update_session_auth_hash,
    authenticate, #user = authenticate(username=user.username, password=raw_password)
    login,
  
)


from django.contrib.auth.forms import PasswordChangeForm
from weather.views import get_string_for_forecast
from api_relay.views import get_user_lat_long_api
from .models import custom_user
from incodaq_weather.dashboard_status_processing import dashboard_status_processing

def sign_up_user(request):
    if request.method == 'POST':
        signup_form_data = user_signup_form(request.POST)
        
        if signup_form_data.is_valid():
            form = signup_form_data.save()
            form.refresh_from_db()
            form.save()
            raw_password = signup_form_data.cleaned_data.get('password1')
            form_login = authenticate(username=form.username, password=raw_password)
            login(request, form_login)
            
            registrationStatus = "You have succesfully registered and have been automatically logged in"
            statusColor = "green"
            user = {"user1": request.user} 
            
            #TODO on variable
            dashboardStatus = {"dashboardStatus": registrationStatus}
            statusColor = {"statusColor": statusColor} 
            
            
            dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor, \
            hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
            hasAddress,hasAddressMessage, hasAddressStatusColor, \
            isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
            wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
            isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor \
            = dashboard_status_processing(**user, **dashboardStatus, **statusColor)
            
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

            #Try to get all possible reasons for errors on registration and show them to user
            try:
                usernameError = ["Username: " + signup_form_data.errors["username"][0]]
            except:
                usernameError = []
            try:
                emailError = ["Email: " + signup_form_data.errors["email"][0]]
            except:
                emailError = []
            try:
                passwordError = ["Password: " + signup_form_data.errors["password2"][0]]
            except:
                passwordError = []

            signup_form_data = user_signup_form()
            registrationStatus = usernameError + emailError + passwordError

            statusColor = "red"
            return render(request, 'signup.html', {'signup_form_data': signup_form_data, 'registrationStatus':registrationStatus, 'statusColor': statusColor})
    else:
        signup_form_data = user_signup_form()
        registrationStatus = ["Please fill the fields located bellow to register"]
        statusColor = "green"
        return render(request, 'signup.html', {'signup_form_data': signup_form_data, 'registrationStatus':registrationStatus, 'statusColor': statusColor})



def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profileFormData = user_profile_form(request.POST, instance = request.user)
            if profileFormData.is_valid(): 
                dataDict = profileFormData.data.dict() #queryDict to python dict
                userAddress = dataDict["userAddress"]
                userCity = dataDict["userCity"]
                userCountry = dataDict["userCountry"]
                userTimeZone = dataDict["userTimeZone"]

                stringForAPILatLong = get_string_for_forecast(userAddress, userCity, userCountry)
                if stringForAPILatLong != "failure":
                    #make api call to get users lat long and if success save it into model
                    apiStatus, userLat, userLong = get_user_lat_long_api(stringForAPILatLong)
                    if apiStatus != "failure":
                        #all checks are succesfull, save userlat,long to model with
                        #new user data and redirect to dashboard
                        manualForm = profileFormData.save(commit=False)
                        manualForm.userLatitude = userLat
                        manualForm.userLongitude = userLong
                        manualForm.save()
                        #User data succesfully saved.
                        return redirect('dashboard')
                    else: 
                        #api call didnt work,dont save anything, return do dashboard and send message to user
                        # 
                        userProfileMessage = "Something went wrong with retrieving forecast location data. Please try again or contact support."
                        messageColor = "red"
                        profileFormData = user_profile_form(instance=request.user)
                        return render (request,'expanded_user/edit_user_profile.html', 
                        {'profileFormData' : profileFormData
                        ,'userProfileMessage': userProfileMessage
                        ,'messageColor': messageColor
                        })

                
                else:
                    # if lat long are in the model delete them because he 
                    # has not got enough info to have lat and long saved
                    #save all other users data and redirect dashboard
                    #Send a message: Not enough data needed for weather forecast
                    try:
                        profileFormData.save()
                        custom_user.objects.filter(pk=request.user.pk).update(
                        userLatitude=""
                        ,userLongitude=""
                        )
                        
                        return redirect('dashboard')
                    except:
                        #saves didnt work,dont save anything and send message to user
                        userProfileMessage = "Not enough data for the forecast. Data was not properly saved. Please try again or contact support."
                        messageColor = "red"
                        profileFormData = user_profile_form(instance=request.user)
                        return render (request,'expanded_user/edit_user_profile.html', 
                        {'profileFormData' : profileFormData
                        ,'userProfileMessage': userProfileMessage
                        ,'messageColor': messageColor
                        })
            else:
                #Form was not validated. Return a proper message to the user.
                userProfileMessage = "Data was not properly validated. Please try again."
                messageColor = "red"
                profileFormData = user_profile_form(instance=request.user)
                return render (request,'expanded_user/edit_user_profile.html', 
                {'profileFormData' : profileFormData
                ,'userProfileMessage': userProfileMessage
                ,'messageColor': messageColor
                })
        
        
        else:
            #Opening the form
            userProfileMessage = "Here you can save location that will be used to determine your forecast."
            messageColor = "green"
            profileFormData = user_profile_form(instance=request.user)
            return render (request,'expanded_user/edit_user_profile.html', 
            {'profileFormData' : profileFormData
            ,'userProfileMessage': userProfileMessage
            ,'messageColor': messageColor
            })
    else:
        return render(request,'index.html')



def edit_user_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password_form_data = PasswordChangeForm(data = request.POST, user = request.user)  
            #PasswordChangeForm  is inbuilt in Django
            currentUser = request.user
            if password_form_data.is_valid():
                password_form_data.save()
                update_session_auth_hash(request, password_form_data.user)
                
                dashboardStatus = {"dashboardStatus": "You have succesfully changed your password."}
                statusColor = {"statusColor": "green"}
                user = {"user1": request.user}
                

                #TODO This is built as a quick fix, review in needed to shorten it and make calling dashboard more reusable
                dashboardStatusMessage,dashboardStatusColor,hasMobileNumber, hasMobileNumberMessage, hasMobileNumberStatusColor, \
                hasCityCountry, hasCityCountryMessage, hasCityCountryStatusColor, \
                hasAddress,hasAddressMessage, hasAddressStatusColor, \
                isMobileValidated, isMobileValidatedMessage, isMobileValidatedStatusColor, \
                wantsToReceiveWeatherSMS, wantsToReceiveWeatherSMSMessage, wantsToReceiveWeatherSMSStatusColor, \
                isForecastTimeSet, isForecastTimeSetMessage, isForecastTimeSetStatusColor \
                = dashboard_status_processing(**user, **dashboardStatus, **statusColor)
            
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
                
                try:
                    oldPasswordError = password_form_data.errors["old_password"]
                except:
                    oldPasswordError = ""
                try:
                    newPasswordError = password_form_data.errors["new_password2"]
                except:
                    newPasswordError = ""


                password_form_data = PasswordChangeForm(user = request.user)
                changePasswordStatus = oldPasswordError + newPasswordError
                statusColor = "red"
                return render (request, 'expanded_user/change_user_password.html', {'password_form_data' : password_form_data, 'changePasswordStatus' : changePasswordStatus, 'statusColor': statusColor})
        else:
            password_form_data = PasswordChangeForm(user = request.user)
            changePasswordStatus = "Hey " + request.user.username + ", please fill the fields bellow to change your password."
            statusColor = "green"
            return render (request, 'expanded_user/change_user_password.html', {'password_form_data' : password_form_data, 'changePasswordStatus': changePasswordStatus, 'statusColor': statusColor })
    else:
        return render(request,'index.html') 
