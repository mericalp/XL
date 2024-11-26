# serializers.py
from rest_framework import serializers
from users.models import EmployeeUser, Attendance, LeaveRequest, CustomUser

class AttendanceSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')
    late_duration = serializers.SerializerMethodField()
    leave_days = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'user_username', 'check_in', 'check_out', 'late_duration', 'leave_days']

    def get_late_duration(self, obj):
        return obj.late_duration()

    def get_leave_days(self, obj):
        employee_profile = EmployeeUser.objects.filter(user=obj.user).first()
        return employee_profile.leave_days if employee_profile else None



            
class DashboardAdminSerializer(serializers.ModelSerializer):
    attendance_data = serializers.SerializerMethodField()
    leave_requests = serializers.SerializerMethodField()
    monthly_reports = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'status', 'attendance_data', 'leave_requests', 'monthly_reports']

    def get_attendance_data(self, obj):
        attendance_data = self.context.get('attendance_data', [])
        return AttendanceSerializer(attendance_data, many=True).data

    def get_leave_requests(self, obj):
        leave_requests = self.context.get('leave_requests', [])
        return LeaveRequestSerializer(leave_requests, many=True).data

    def get_monthly_reports(self, obj):
        monthly_reports = self.context.get('monthly_reports', [])
        return monthly_reports.values('user__username').annotate(
            total_hours=Count('id') * 8,
            total_late_minutes=Sum('late_duration')
        )