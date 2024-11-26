from django.urls import path
from .views import AttendanceView, AttendanceAPI, LeaveView, LeaveAPI

urlpatterns = [
    path('attendance/', AttendanceView.as_view(), name='attendance_view'),
    path('api/attendance/', AttendanceAPI.as_view(), name='attendance_api'),
    path('request-leave/', LeaveView.as_view(), name='request_leave'),  # Updated name
    path('api/leave-requests/', LeaveAPI.as_view(), name='leave_requests_api'),
]