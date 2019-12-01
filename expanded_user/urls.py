from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.sign_up_user, name='signup'),
    path('', include('social_django.urls', namespace='social')),
    path('profile/edit-user-profile/', views.edit_user_profile, name='edit_user_profile'),


    path('profile/edit-password/', views.edit_user_password, name='edit_user_password'),

    path('profile/password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

  #  path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
  #  path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # these urls use password change html registration/password_change_form.html

    
]