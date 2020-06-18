from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import custom_user
from incodaq_weather.choice import WORLD_TIME_ZONES


class user_signup_form(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': ''}))
    # first_name = forms.CharField(help_text='Required')
    # last_name = forms.CharField(help_text='Required')
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': ''}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': ''}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': ''}))

    class Meta:
        model = custom_user
        fields = (
            'username',
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            'password2',
        )


class user_profile_form(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'readonly': 'readonly', 'class': 'form-control'}))
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    userAddress = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    userCity = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    userCountry = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    userTimeZone = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'form-control'}), choices=WORLD_TIME_ZONES, )

    class Meta:
        model = custom_user
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            # 'userSecondEmail',
            'userCountry',
            'userCity',
            'userAddress',
            'userTimeZone',
        )


# class custom_user_change_form - form used in the admin interface to change a user’s information and permissions.
class custom_user_change_form(UserChangeForm):
    class Meta:
        model = custom_user
        fields = ('username', 'email')