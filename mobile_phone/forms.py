from django import forms
from .models import user_phone
from incodaq_weather.choice import FORECAST_HOURS, MOBILE_PHONE_COUNTY_CODE


class user_mobile_phone_form(forms.ModelForm):
    #userMobilePhone = forms.CharField(label='', widget=forms.TextInput(attrs={'readonly':'readonly','class':'form-control'}))
    phoneCountryCode = forms.ChoiceField(required=False, widget=forms.Select, choices=MOBILE_PHONE_COUNTY_CODE,)
    phoneNumber = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    wantsToReceiveWeatherSMS = forms.BooleanField(required=False)
    timeWeatherSMS = forms.ChoiceField(required=False, widget=forms.Select, choices=FORECAST_HOURS,)
    class Meta:
        model = user_phone
        fields = (
            #'userMobilePhone',
            'phoneCountryCode',
            'phoneNumber',
            'wantsToReceiveWeatherSMS',
            'timeWeatherSMS',
)