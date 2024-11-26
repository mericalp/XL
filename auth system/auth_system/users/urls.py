# users/urls.py
from django.urls import path
from .AuthenticationAPI import AuthenticationAPI
from .AuthenticationView import AuthenticationView

urlpatterns = [
    # API endpoints
    path('api/auth/<str:action>/', AuthenticationAPI.as_view(), name='auth_api'),
    
    # Web endpoints
    path('auth/<str:action>/', AuthenticationView.as_view(), name='auth'),
    path('auth/profile/<str:username>/', 
         AuthenticationView.as_view(), 
         kwargs={'action': 'profile'}, 
         name='profile'),
         
    # Function-based views
    path('activate/<str:uidb64>/<str:token>/', 
         AuthenticationView.as_view(),
         kwargs={'action': 'activate'},
         name='activate'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/',
         AuthenticationView.as_view(),
         kwargs={'action': 'reset_confirm'},
         name='password_reset_confirm'),
    path('logout/',
         AuthenticationView.as_view(),
         kwargs={'action': 'logout'},
         name='logout'),
 
     # Admin routes
    path('auth/admin/login/', 
         AuthenticationView.as_view(), 
         kwargs={'action': 'login', 'type': 'admin'}, 
         name='admin_login'),
    path('auth/admin/register/', 
         AuthenticationView.as_view(), 
         kwargs={'action': 'signup', 'type': 'admin'}, 
         name='admin_register'),

    # Employee routes  
    path('auth/employee/login/',
         AuthenticationView.as_view(),
         kwargs={'action': 'login', 'type': 'employee'},
         name='login'),
    path('auth/employee/register/',
         AuthenticationView.as_view(),
         kwargs={'action': 'signup', 'type': 'employee'},
         name='register'),

     # # Admin-specific routes
     # path('auth/admin/login/', AuthenticationView.as_view(), kwargs={'action': 'login', 'type': 'admin'}, name='admin_login'),
     # path('auth/admin/register/', AuthenticationView.as_view(), kwargs={'action': 'signup', 'type': 'admin'}, name='admin_register'),

     # # Employee-specific routes
     # path('auth/employee/login/', AuthenticationView.as_view(), kwargs={'action': 'login', 'type': 'employee'}, name='employee_login'),
     # path('auth/employee/register/', AuthenticationView.as_view(), kwargs={'action': 'signup', 'type': 'employee'}, name='employee_register'),

     # # API endpoints
     # path('api/auth/<str:action>/', AuthenticationAPI.as_view(), name='auth_api'),

]

# urlpatterns = [
#     # Web endpoints
#     path('auth/login/', 
#          AuthenticationView.as_view(), 
#          kwargs={'action': 'login'}, 
#          name='login'),  # Add explicit login URL
         
#     path('auth/<str:action>/', 
#          AuthenticationView.as_view(), 
#          name='auth'),
         
#     path('auth/profile/<str:username>/', 
#          AuthenticationView.as_view(), 
#          kwargs={'action': 'profile'}, 
#          name='profile'),
         
#     path('logout/',
#          AuthenticationView.as_view(),
#          kwargs={'action': 'logout'},
#          name='logout'),
         
#     # API endpoints
#     path('api/auth/<str:action>/', 
#          AuthenticationAPI.as_view(), 
#          name='auth_api'),
# ]