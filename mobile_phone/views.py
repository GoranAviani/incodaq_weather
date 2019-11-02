from django.shortcuts import render, redirect

# Create your views here.
from .forms import (
    user_mobile_phone_form
)
from .models import (
    user_phone
)

from expanded_user.models import custom_user

def is_mobile_still_validated(oldPhoneNumber, newPhoneNumber):
    if newPhoneNumber.isdigit():

        if len(newPhoneNumber) < 4:
            return False
        
        if oldPhoneNumber != newPhoneNumber:
            return False
            
        return True
    else:
        return False    
    

    
def edit_user_phone(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_phone_form_data = user_mobile_phone_form(request.POST.copy()) #.copy() because query dict would be immutable
          
            try:
                #if this user is found in user phone model ergo already has his phone number here
                found_u_p_data = user_phone.objects.get(userMobilePhone=request.user) 
                if user_phone_form_data.is_valid():
                    
                    #Simple check should the phone still be validated: Sto see if user hasis_mobile_still_validated changed a phone number or is it
                    # wrong is some other sence, if so he can no longer have a validated number
                    isMobileStillValidated = is_mobile_still_validated(found_u_p_data.phoneNumber, user_phone_form_data["phoneNumber"].data)

                    user_phone.objects.filter(userMobilePhone=request.user).update(phoneCountryCode=user_phone_form_data["phoneCountryCode"].data
                    , phoneNumber=user_phone_form_data["phoneNumber"].data
                    , wantsToReceiveWeatherSMS=user_phone_form_data["wantsToReceiveWeatherSMS"].data
                    , timeWeatherSMS=user_phone_form_data["timeWeatherSMS"].data
                    , isMobileValidated = isMobileStillValidated)
                    #, wantsToReceiveWeatherSMS=user_mobile_phone_form["wantsToReceiveWeatherSMS"].data)
                #else goes to  else: try: except: bellow because either  way (succes or failure) 
                # it gets redirected return redirect('edit_mobile_phone' 
            except:
                aa = custom_user.objects.get(pk=request.user.pk)
                user_phone_form_data.data["userMobilePhone"] = aa # Need custom user object to work
                if user_phone_form_data.is_valid():
                    form = user_phone_form_data.save(commit=False)
                    form.userMobilePhone = request.user
                    form.save()
            return redirect('dashboard')
        else:
            try:
                found_u_p_data = user_phone.objects.get(userMobilePhone=request.user)
                data = {'userMobilePhone':found_u_p_data.userMobilePhone 
                ,'phoneCountryCode': found_u_p_data.phoneCountryCode 
                ,"phoneNumber": found_u_p_data.phoneNumber
                ,"wantsToReceiveWeatherSMS": found_u_p_data.wantsToReceiveWeatherSMS
                ,"timeWeatherSMS": found_u_p_data.timeWeatherSMS
                }
                user_phone_form_data = user_mobile_phone_form(initial=data)
            except:
                user_phone_form_data = user_mobile_phone_form()
            
            return render (request, 'mobile_phone/edit_user_phone.html', {'user_phone_form_data' : user_phone_form_data})
    else:
        return render(request,'index.html')