
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .decorators import user_is_superuser
import os
from uuid import uuid4
from django.utils import timezone
from users.models import Attendance, CustomUser, LeaveRequest
from django.http import JsonResponse
from datetime import datetime  
from business_logic.businessAPI import EntityAPI
from business_logic.businessView import EntityView
from .serializers import AttendanceSerializer, LeaveRequestSerializer
from django.utils.decorators import method_decorator
from .forms import AttendanceForm


class AttendanceView(EntityView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "main/home.html"
    filter_by_user = True
    context_object_name = 'attendance'

    def apply_custom_filters(self, queryset, request):
        today = timezone.now().date()
        return queryset.filter(date=today)

class AttendanceAPI(EntityAPI):
    model = Attendance
    serializer_class = AttendanceSerializer
    filter_by_user = True
    filter_fields = ['date']

    def get_existing_record(self, request, data):
        date = data.get('date')
        return self.model.objects.filter(
            user=request.user,
            date=date
        ).first()

class LeaveAPI(EntityAPI):
    model = LeaveRequest
    serializer_class = LeaveRequestSerializer
    filter_by_user = False

    def get_existing_record(self, request, data):
        leave_id = data.get('leave_id')
        if leave_id:
            return self.model.objects.filter(id=leave_id).first()
        return None

class LeaveView(EntityView):
    model = LeaveRequest
    template_name = "main/request_leave.html"
    filter_by_user = True
    context_object_name = 'leave_requests'

    def apply_custom_filters(self, queryset, request):
        return queryset.filter(approved=False)