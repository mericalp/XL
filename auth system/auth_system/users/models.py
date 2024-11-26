from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os 
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class CustomUser(AbstractUser):
    STATUS = (
        ('employee', 'employee'),
        ('admin', 'admin'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='employee')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    
    def __str__(self):
        return self.username


class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    admin_role = models.CharField(max_length=100, default='Default Admin Role')

    def __str__(self):
        return f"Admin: {self.user.username}"


class EmployeeUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    leave_days = models.IntegerField(default=15)

    def __str__(self):
        return f"Employee: {self.user.username}"


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
     
    
    def send_late_email_to_admins(self, minutes):
        try:
            # Fetch all users with status='admin'
            admin_users = CustomUser.objects.filter(status='admin')

            # Iterate over each admin and send email
            for admin in admin_users:
                subject = f"⚠️ Late Arrival Notification for {self.user.username}"
                message = render_to_string("late_notification.html", {
                    'admin': admin,
                    'user': self.user,
                    'date': self.date,
                    'minutes': int(minutes),
                })
                email = EmailMessage(subject, message, to=[admin.email])
                email.send()
        except Exception as e:
            print(f"Email error: {str(e)}")
            
    def is_late(self):
        if self.check_in and self.check_in > timezone.datetime.strptime('08:00', '%H:%M').time():
            return True
        return False

    def late_duration(self):
        if self.is_late():
            late_time = timezone.datetime.combine(self.date, self.check_in) - \
                        timezone.datetime.combine(self.date, timezone.datetime.strptime('08:00', '%H:%M').time())
            minutes = late_time.total_seconds() / 60
            # Send email notification to all admins
            self.send_late_email_to_admins(minutes)

            # Send notification via WebSocket
            # self.send_late_notification(minutes) 
            return minutes
  

class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(null=True)  # Allow null for pending status

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date}"

    def calculate_leave_days(self):
        """Calculate the total number of leave days."""
        return (self.end_date - self.start_date).days + 1
    
    def deduct_leave_days(self):
        """Deduct leave days from the user's available leave."""
        leave_days = self.calculate_leave_days()
        employee_profile = EmployeeUser.objects.filter(user=self.user).first()
        if employee_profile and employee_profile.leave_days >= leave_days:
            employee_profile.leave_days -= leave_days
            employee_profile.save()

            # Notify admin if leave days fall below 3
            if employee_profile.leave_days < 3:
                self.notify_admin_of_low_leave()
        elif employee_profile:
            raise ValueError(f"Not enough leave days for {self.user.username}")

    def notify_admin_of_low_leave(self):
        """Notify admins when an employee has less than 3 leave days."""
        admin_users = AdminUser.objects.all()
        for admin in admin_users:
            print(f"Notification sent to {admin.user.username}: {self.user.username} has less than 3 leave days remaining.")
