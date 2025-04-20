
import re
from rest_framework import serializers
from .models import User
from django.shortcuts import get_object_or_404
from .utils import generate_otp, store_otp, verify_otp

def validate_phone_number_format(value):
    """
    Validate that the phone number matches the required pattern.
    """
    pattern = r'^09(1[0-9]|2[0-2]|3[0-9]|9[0-4])[0-9]{7}$'
    
    if not re.match(pattern, value):
        raise serializers.ValidationError("Please enter a valid mobile number.")
        
    return value


# OK
class PhoneNumberSerializer(serializers.Serializer): #1
    phone_number = serializers.CharField(max_length=11)
    
    def validate_phone_number(self, value):
        return validate_phone_number_format(value)
    
    
    
    
# OK
class OTPVerificationSerializer(serializers.Serializer): #2
    # phone_number = serializers.CharField(max_length=11)
    otp = serializers.CharField(max_length=6)
    
    # def validate_phone_number(self, value):
    #     return validate_phone_number_format(value)
    
    #  # Method to generate and send OTP
    # def generate_and_send_otp(self, phone_number):
    #     otp = generate_otp()
    #     store_otp(phone_number, otp)
    #     message = f"Your verification code is: {otp}"
    #     send_sms(phone_number, message)
    #     return otp
    
    def validate_otp(self, value):
        otp = value
        
        if not verify_otp(otp):
            raise serializers.ValidationError({"otp": "Invalid or expired OTP"})
        
        return value
    
    
    # def validate(self, data):
    #     phone_number = data.get('phone_number')
    #     otp = data.get('otp')
        
    #     # Verify the OTP matches what was stored
    #     if not verify_otp(phone_number, otp):
    #         raise serializers.ValidationError({"otp": "Invalid or expired OTP"})
            
    #     return data
    
# OK 
class PasswordAuthSerializer(serializers.Serializer): #5
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=11, write_only=True)
    
    def validate_phone_number(self, value):
        return validate_phone_number_format(value)
    
# OK 
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
    
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        return value


# OK   
class UserRegisterSerializer(serializers.Serializer): #4
    password = serializers.CharField(max_length = 128, write_only = True)
    
    def validate_password(self, value):
        """
        Validate password complexity using regex.
        """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-#])[A-Za-z\d@$!%*?&_\-#]{8,}$'
        
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain at least "
                "one uppercase letter, one lowercase letter, one digit, and one special character."
            )
            
        return value

