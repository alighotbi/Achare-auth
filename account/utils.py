import random
import string
from django.conf import settings
from django.core.cache import cache

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def store_otp(phone_number, otp):
    cache_key = f"otp_{phone_number}"
    expiry_time = getattr(settings, "OTP_EXPIRY_TIME", 300)
    cache.set(cache_key, otp, expiry_time)
    
def verify_otp(phone_number, otp):
    """
    Verify if the provided OTP matches the one stored for the given phone number."""
        
    cache_key = f"otp_{phone_number}"
    stored_otp = cache.get(cache_key)
    
    # Check if stored_otp exists and matches the provided otp
    if stored_otp and stored_otp == otp:
        # Delete the OTP from cache after successful verification
        # to prevent reuse
        cache.delete(cache_key)
        return True
    
    return False


def send_sms(phone_number, message):
    """
    Placeholder for SMS sending functionality.
    In a real application, this would integrate with an SMS service provider.
    """
    # In a real application, you would integrate with Twilio, Vonage, etc.
    print(f"Sending SMS to {phone_number}: {message}")
    # For now, we'll just return True to simulate successful sending
    return True 
