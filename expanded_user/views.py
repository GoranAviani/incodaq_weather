from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from .forms import (
    user_signup_form,
    
)

from django.contrib.auth import (
    update_session_auth_hash,
    authenticate, #user = authenticate(username=user.username, password=raw_password)
    login,
  
)


def sign_up_user(request):
    if request.method == 'POST':
        signup_form = user_signup_form(request.POST)
        
        if signup_form.is_valid():
            form = signup_form.save()
            form.refresh_from_db()
            form.save()
            raw_password = signup_form.cleaned_data.get('password1')
            form_login = authenticate(username=form.username, password=raw_password)
            login(request, form_login)
            registrationStatus = "You have succesfully registered and have been automatically logged in"
            statusColor = "green"
            return render(request, 'dashboard.html', {'dashboardStatus':registrationStatus, 'statusColor': statusColor})

        else:

            #Try to get all possible reasons for errors on registration and show them to user
            try:
                usernameError = signup_form.errors["username"]
            except:
                usernamelError = ""
            try:
                emailError = signup_form.errors["email"]
            except:
                emailError = ""
            try:
                passwordError = signup_form.errors["password2"]
            except:
                passwordError = ""

            signup_form = user_signup_form()
            registrationStatus = usernameError + emailError + passwordError
            statusColor = "red"
            return render(request, 'signup.html', {'signup_form': signup_form, 'registrationStatus':registrationStatus, 'statusColor': statusColor})
    else:
        signup_form = user_signup_form()
        registrationStatus = "Please fill the fields located bellow to register"
        statusColor = "green"
        return render(request, 'signup.html', {'signup_form': signup_form, 'registrationStatus':registrationStatus, 'statusColor': statusColor})



def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_form_data = user_profile_form(request.POST, instance = request.user)
            if profile_form_data.is_valid():
                profile_form_data.save()
                return redirect('dashboard')
        else:
            profile_form_data = user_profile_form(instance=request.user)
            return render (request, 'expanded_user/edit_user_profile.html', {'profile_form_data' : profile_form_data})
    else:
        return render(request,'index.html')