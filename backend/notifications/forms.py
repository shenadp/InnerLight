from django import forms
from .models import NotificationSchedule, DoNotDisturb
from accounts.widgets import ToggleWidget, StyledTimeInput

class NotificationScheduleForm(forms.ModelForm):
    scheduled_time = forms.TimeField(
        widget=StyledTimeInput(attrs={'type': 'time'}),
        label='Reminder Time'
    )
    is_active = forms.BooleanField(
        required=False,
        label='Enable this reminder',
        widget=ToggleWidget()
    )

    class Meta:
        model = NotificationSchedule
        fields = ['notif_type', 'scheduled_time', 'is_active']


class DoNotDisturbForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=StyledTimeInput(attrs={'type': 'time'}),
        label='DND Start Time'
    )
    end_time = forms.TimeField(
        widget=StyledTimeInput(attrs={'type': 'time'}),
        label='DND End Time'
    )
    is_active = forms.BooleanField(
        required=False,
        label='Enable Do Not Disturb',
        widget=ToggleWidget()
    )

    class Meta:
        model = DoNotDisturb
        fields = ['is_active', 'start_time', 'end_time']