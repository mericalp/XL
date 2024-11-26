from django.urls import path
from .views import DashboardAdminAPI, DashboardAdminView, LeaveRequestView, MonthlyReportAPI, MonthlyReportView

urlpatterns = [
    path('admin/dashboard/', DashboardAdminView.as_view(), name='admin_dashboard'),
    path('api/admin/dashboard/', DashboardAdminAPI.as_view(), name='admin_dashboard_api'),
    path('admin/leave-requests/', LeaveRequestView.as_view(), name='leave_requests'),
    path('admin/monthly-reports/', MonthlyReportView.as_view(), name='monthly_reports'),
    path('api/admin/monthly-reports/', MonthlyReportAPI.as_view(), name='monthly_reports_api'),
]

