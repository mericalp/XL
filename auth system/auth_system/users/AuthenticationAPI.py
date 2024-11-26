from logging.config import valid_ident
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q

from .forms import SignupForm, SignInForm, UserInfoUpdate, UpdatePass
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from .serializers import  UserSerializer, LoginSerializer, SignupSerializer, PasswordChangeSerializer, UserProfileSerializer
 
# authentication/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import AdminUser, EmployeeUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticationAPI(APIView):
    action_map = {
        'login': 'handle_login',
        'signup': 'handle_signup',
        'reset_password': 'handle_reset_password',
        'change_password': 'handle_change_password',
        'profile': 'handle_profile',
        'activate': 'handle_activate',
        'logout': 'handle_logout'
    }

    def post(self, request, action=None):
        handler = getattr(self, self.action_map.get(action, 'handle_invalid'))
        return handler(request)
    

    def handle_login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)
        
        user = serializer.validated_data['user']
        
        # Determine user_type from the status field
        if user.status == 'admin':
            user_type = 'admin'
        elif user.status == 'employee':
            user_type = 'employee'
        else:
            return self.error_response("Invalid user type")  # Handle unexpected user types
        
        login(request, user)

        # Serialize user data and include the user_type explicitly
        user_data = UserSerializer(user).data
        user_data['user_type'] = user_type  # Add user_type to the serialized response

        return self.success_response("Login successful", user_data)

    def handle_signup(self, request):
        user_type = request.data.get('user_type')
        if user_type not in ['admin', 'employee']:
            return self.error_response("Invalid user type")
            
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)  # Return detailed validation errors
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        user = serializer.save()
        
        # Create profile based on user type
        if user_type == 'admin':
            AdminUser.objects.create(user=user)
            user.status = 'admin'
        else:
            EmployeeUser.objects.create(user=user)
            user.status = 'employee'
        
        user.save()
        self.send_activation_email(request, user)
        return self.success_response("Please check your email to activate your account")
 

    def handle_logout(self, request):
        logout(request)
        return self.success_response("Logged out successfully")

    def success_response(self, message, data=None):
        response = {"message": message}
        if data:
            response["data"] = data
        return Response(response)

    def error_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"error": message}, status=status_code)

    def send_activation_email(self, request, user):
        subject = "Activate Your Account"
        message = render_to_string("account_activat_temp.html", {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.send()