from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import user_phone


class user_mobile_admin (admin.ModelAdmin):
    list_display = ("phoneCountryCode" , "phoneNumber" , "isMobileValidated","sendWeatherSMS")
    list_filter = ("phoneCountryCode", "phoneNumber" , "isMobileValidated","sendWeatherSMS")
    search_fields= ("phoneCountryCode","phoneNumber", "isMobileValidated","sendWeatherSMS")


admin.site.register(user_phone, user_mobile_admin)