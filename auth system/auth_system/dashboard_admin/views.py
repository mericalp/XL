from django.shortcuts import render
from users.models import Attendance, CustomUser, LeaveRequest
from business_logic.businessView import EntityView
from business_logic.businessAPI import EntityAPI
from .serializers import AttendanceSerializer, DashboardAdminSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from business_logic.businessView import EntityView
from users.models import Attendance, LeaveRequest, EmployeeUser
from django.shortcuts import redirect
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DurationField, Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from rest_framework.response import Response
from users.models import Attendance, LeaveRequest
from rest_framework import status
import logging


logger = logging.getLogger(__name__)


class DashboardAdminView(EntityView):
    model = CustomUser
    template_name = "main/admin_dashboard.html"
    context_object_name = 'dashboard_data'

    def apply_custom_filters(self, queryset, request):
        if not request.user.is_authenticated or request.user.status != 'admin':
            return redirect('login')
            
        today = timezone.now().date()
        today_attendance = Attendance.objects.filter(date=today).select_related('user')
        
        return {
            'attendances': today_attendance
        }

class DashboardAdminAPI(EntityAPI):
    model = Attendance
    serializer_class = AttendanceSerializer
    filter_by_user = False

    def get_existing_record(self, request, data):
        today = timezone.now().date()
        return self.model.objects.filter(date=today).select_related('user')


class LeaveRequestView(EntityView):
    model = LeaveRequest
    template_name = "main/leave_request.html"
    context_object_name = 'leave_requests'

    def apply_custom_filters(self, queryset, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return queryset.filter(approved=False)

class MonthlyReportView(EntityView):
    model = Attendance 
    template_name = "main/monthly_reports.html"
    context_object_name = 'reports'

    def apply_custom_filters(self, queryset, request):
        current_month = timezone.now().month
        return queryset.filter(date__month=current_month)

class MonthlyReportAPI(EntityAPI):
    model = Attendance
    serializer_class = AttendanceSerializer

    def get_existing_record(self, request, data):
        current_month = timezone.now().month
        return self.model.objects.filter(date__month=current_month)