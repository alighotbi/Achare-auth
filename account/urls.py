from django.urls import path
from .views import (
    InitiatePhoneNumber,
    RegisterOTPView,
    CompletProfileInfoView,
    RegisterPasswordView,
    LoginView,
)

app_name = 'account'

urlpatterns = [
    # Step 1: User enters phone number
    path('initiate/', InitiatePhoneNumber.as_view(), name='initiate-phone'),
    
    # Step 2a: For new users - verify OTP and register Their phone number
    path('verify-otp/', RegisterOTPView.as_view(), name='verify-otp'),
    
    # Step 2b: For existing users - login with password
    path('login/', LoginView.as_view(), name='login'),
    
    # Step 3: Complete profile with personal information
    path('complete-profile/', CompletProfileInfoView.as_view(), name='complete-profile'),
    
    # Step 4: Set password for new users
    path('set-password/', RegisterPasswordView.as_view(), name='set-password'),
]