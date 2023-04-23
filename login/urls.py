from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('send_otp/', send_otp),
    path('register/', register),
    path('login/', login),
    path('validate_username/', validate_username),
    path('update_profile/', update_profile),
    path('users/', users),
    path('delete_user/', delete_user),
    path('reset_password/', reset_password),

    path('user_addresses/', user_addresses),
    path('add_user_address/', add_user_address),
    path('update_user_address/', update_user_address),
    path('delete_user_address/', delete_user_address),

    path('register_provider/', register_provider),
    path('provider_info/', provider_info),
    path('providers/', providers),
    path('update_provider/', update_provider),
    path('delete_provider/', delete_provider),

    path('update_user_role/', update_user_role),
    
    path('send_otp_to_email/', send_otp_to_email),
    path('send_smtp_email/', send_smtp_email),
    
]