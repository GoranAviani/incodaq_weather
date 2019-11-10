from django.contrib import admin

# Register your models here.

from .models import default_cities


class default_cities_admin (admin.ModelAdmin):
    list_display = ("Stockholm" , "Tokyo")
    #list_filter = ("phoneCountryCode", "phoneNumber" , "isMobileValidated","wantsToReceiveWeatherSMS")
    #search_fields= ("phoneCountryCode","phoneNumber", "isMobileValidated","wantsToReceiveWeatherSMS")


admin.site.register(default_cities, default_cities_admin)