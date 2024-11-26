from users.models import Attendance, LeaveRequest

from django import forms

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out']


class LeaveRequestForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'start-date'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'end-date'})
    )

    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date")
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past")

        return cleaned_data