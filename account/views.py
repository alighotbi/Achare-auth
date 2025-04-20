from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .models import User
from .serializers import (
    PhoneNumberSerializer, 
    OTPVerificationSerializer, 
    PasswordAuthSerializer,
    UserInfoSerializer,
    UserRegisterSerializer,
)
from .utils import (
    generate_otp,
    store_otp,
    verify_otp,
    store_phone_number,
    get_phone_number,
)

from .decoraors import ip_rate_limit

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

# OK
class InitiatePhoneNumber(APIView):
    
        @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: OpenApiExample(
                'Success',
                value={'message': 'OTP sent successfully. Please verify to complete registration.'}
            ),
            302: OpenApiExample(
                'User Exists',
                value={'message': 'You will redirect to login page.'}
            ),
            400: OpenApiExample(
                'Invalid Input',
                value={'phone_number': ['Please enter a valid mobile number.']}
            ),
        },
        description='Send OTP to a phone number for verification. If the user is already registered, they will be redirected to login.',
        summary='Initiate phone number verification',
    )
    
        def post(self, request):
            serializer = PhoneNumberSerializer(data=request.data)
            if serializer.is_valid():
                phone_number = serializer.validated_data['phone_number']
            
            user_exists = User.objects.filter(phone_number=phone_number).exists()
            if user_exists:
                return Response({"message": "You will redirect to login page."}, status=status.HTTP_200_OK)
            
            if not user_exists:
                otp = generate_otp()
                store_otp(otp)
                store_phone_number(phone_number)
                
                # message = f"Your verification code is: {otp}"
                # send_sms(phone_number, message)
                
                return Response(
                    f"OTP: {otp} sent successfully. Please verify to complete registration.", status=status.HTTP_200_OK
                )
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# OK
class LoginView(APIView):
    @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: OpenApiExample(
                'Success',
                value={'refresh': 'refresh_token', 'access': 'access_token'}
            ),
            400: OpenApiExample(
                'Invalid Input',
                value={'phone_number': ['Please enter a valid mobile number.']}
            ),
        },
        description='Authenticate a user with phone number and password.',
        summary='Authenticate user with phone number and password',
    )
    
    @ip_rate_limit(view_type="login", limit=3, timeout=3600)
    def post(self, request):
        serializer = PasswordAuthSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
                
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RegisterOTPView(APIView):
    
    @extend_schema(
        request=OTPVerificationSerializer,
        responses={
            201: OpenApiExample(
                'Success',
                value={'message': 'OTP verified successfully. Please complete your profile.', 'refresh': 'refresh_token', 'access': 'access_token'}
            )})
    @ip_rate_limit(view_type="otp", limit=3, timeout=3600)
    def post(self, request):
         serializer = OTPVerificationSerializer(data=request.data)
         if serializer.is_valid():
            phone_number = get_phone_number()
            if not phone_number:
                return Response({'message': 'Phone number not found or expired., Please restart the verification process'}, status=status.HTTP_404_NOT_FOUND)
            
            user = User.objects.create_user(phone_number=phone_number, is_active = True, password=None)
            user.save()
            cache.delete(phone_number)
                
                # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
                
            return Response({
                    'message': 'OTP verified successfully. Please complete your profile.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED)
         
         # Added return statement for invalid data
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# OK
class CompletProfileInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request):
        user = request.user
        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message': 'Profile Updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
# OK   
class RegisterPasswordView(APIView):
    #  permission_classes = [permissions.IsAuthenticated]
     
     def put(self, request):
         user = request.user
         serializer = UserRegisterSerializer(user, data=request.data, partial=True)
         if serializer.is_valid():
             user.set_password(serializer.validated_data['password'])
             user.save()
             
             return Response({
                 'message': 'Password updated successfully'
             }, status=status.HTTP_200_OK)
              
         return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)