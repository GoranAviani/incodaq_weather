from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from .forms import (
    user_signup_form,
    
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
            return redirect('dashboard')
        else:
            signup_form = user_signup_form()
            return render(request, 'signup.html', {'signup_form': signup_form})

    else:
        signup_form = user_signup_form()
        return render(request, 'signup.html', {'signup_form': signup_form})

