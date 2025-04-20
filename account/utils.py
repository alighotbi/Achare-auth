import random
import string
from django.conf import settings
from django.core.cache import cache

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# def store_otp(phone_number, otp):
#     cache_key = f"otp_{phone_number}"
#     expiry_time = getattr(settings, "OTP_EXPIRY_TIME", 300)
#     cache.set(cache_key, otp, expiry_time)

def store_otp(otp):
    cache_key = "OTP is: "
    cache.set(cache_key, otp, 300)
    
def verify_otp(otp):
    """
    Verify if the provided OTP matches the one stored for the given phone number."""
        
    cache_key = "OTP is: "
    stored_otp = cache.get(cache_key)
    
    # Check if stored_otp exists and matches the provided otp
    if stored_otp and stored_otp == otp:
        # Delete the OTP from cache after successful verification
        # to prevent reuse
        cache.delete(cache_key)
        return True
    
    return False

def store_phone_number(phone_number):
    cache_key = "phone_number"
    cache.set(cache_key, phone_number, 300)
    
def get_phone_number():
    cache_key = "phone_number"
    return cache.get(cache_key)


def get_client_ip(request):
    """Extract real IP even if behind proxy (optional)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# def send_sms(phone_number, message):
#     """
#     Placeholder for SMS sending functionality.
#     In a real application, this would integrate with an SMS service provider.
#     """
#     # In a real application, you would integrate with Twilio, Vonage, etc.
#     print(f"Sending SMS to {phone_number}: {message}")
#     # For now, we'll just return True to simulate successful sending
#     return True 
