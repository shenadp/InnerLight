from django import forms
from .models import Habit, HabitLog
from accounts.widgets import ToggleWidget, StyledTimeInput

class HabitForm(forms.ModelForm):
    custom_days = forms.MultipleChoiceField(
        choices=[
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
            ('Sun', 'Sunday'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Custom Days (if frequency is Custom)'
    )
    reminder_time = forms.TimeField(
        required=False,
        widget=StyledTimeInput(attrs={'type': 'time'}),
        label='Reminder Time'
    )
    goal_duration = forms.IntegerField(
        required=False,
        min_value=1,
        label='Goal Duration (minutes)'
    )
    goal_count = forms.IntegerField(
        required=False,
        min_value=1,
        label='Goal Count'
    )

    class Meta:
        model = Habit
        fields = [
            'name',
            'icon',
            'color',
            'frequency',
            'custom_days',
            'category',
            'reminder_time',
            'goal_duration',
            'goal_count',
        ]


class HabitLogForm(forms.ModelForm):
    note = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Quick note...'}),
        label='Note (optional)'
    )

    class Meta:
        model = HabitLog
        fields = ['completion', 'note']