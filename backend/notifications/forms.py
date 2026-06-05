from django import forms
from .models import NotificationSchedule, DoNotDisturb

class NotificationScheduleForm(forms.ModelForm):
    scheduled_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Reminder Time'
    )
    is_active = forms.BooleanField(
        required=False,
        label='Enable this reminder'
    )

    class Meta:
        model = NotificationSchedule
        fields = [
            'notif_type',
            'scheduled_time',
            'is_active',
        ]


class DoNotDisturbForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='DND Start Time'
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='DND End Time'
    )
    is_active = forms.BooleanField(
        required=False,
        label='Enable Do Not Disturb'
    )

    class Meta:
        model = DoNotDisturb
        fields = [
            'is_active',
            'start_time',
            'end_time',
        ]