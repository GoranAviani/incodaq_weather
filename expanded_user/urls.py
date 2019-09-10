from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.sign_up_user, name='signup'),
    path('profile/edit-user-profile/', views.edit_user_profile, name='edit_user_profile'),
    
]