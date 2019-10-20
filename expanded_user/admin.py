from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import user_signup_form, custom_user_change_form
from .models import custom_user

class custom_user_admin(UserAdmin):
    add_form = user_signup_form
    form = custom_user_change_form
    model = custom_user
    #list_display = ['username','email','userMobilenumber','first_name', 'last_name','is_active','is_staff','is_superuser','last_login','userCountry' ]
    list_display = ['username','email','first_name', 'last_name','is_active','is_staff','is_superuser','last_login','userCountry' ]
    
    fieldsets = (
    (None, {'fields': ('username', 'email', 'password')}),
   ('Basic info', {'fields': ( 'first_name', 'last_name')}),
    ('Other info', {'fields': ('userCity', 'userCountry','userTimeZone','userLatitude', 'userLongitude')}),

    #('Other info', {'fields': ( 'userMobilenumber','userCity', 'userCountry')}),
  ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active','groups')}),
        ('Important dates', {'fields': ( 'last_login', 'date_joined')}),
   )

admin.site.register(custom_user, custom_user_admin)