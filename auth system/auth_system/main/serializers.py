 
from rest_framework import serializers
from users.models import Attendance, LeaveRequest
from datetime import datetime
from django.utils import timezone



class LeaveRequestSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'user_username', 'start_date', 'end_date', 'approved']
       
    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError({
                    "end_date": "End date must be after start date."
                })
        return data

    def update(self, instance, validated_data):
        instance.approved = validated_data.get('approved', instance.approved)
        instance.save()
        if instance.approved:
            instance.deduct_leave_days()
        return instance


class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "iso-8601"])

    class Meta:
        model = Attendance
        fields = ['user', 'date', 'check_in', 'check_out']

    def validate_date(self, value):
        if isinstance(value, datetime):
            return value.date()
        return value