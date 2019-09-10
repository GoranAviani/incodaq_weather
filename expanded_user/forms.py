from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import custom_user

YEARS= [year for year in range(1940,2010)]


class user_signup_form(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    #first_name = forms.CharField(help_text='Required')
    #last_name = forms.CharField(help_text='Required')
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = custom_user
        fields = (
            'username',
            #'first_name',
            #'last_name',
            'email',
            'password1',
            'password2',
)


class user_profile_form(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    userDoB =  forms.DateField(label='', widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = custom_user
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            #'userSecondEmail',
            'userDoB',
            'userCountry',
            'userCity',
            'userAddress',
)
