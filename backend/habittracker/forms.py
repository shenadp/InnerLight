from django import forms
from .models import Habit, HabitLog
from accounts.widgets import (
    ToggleWidget, StyledTimeInput, StyledTextInput,
    StyledNumberInput, StyledSelect
)

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
        widget=forms.CheckboxSelectMultiple(),
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
        label='Goal Duration (minutes)',
        widget=StyledNumberInput(attrs={'placeholder': 'e.g. 30'})
    )
    goal_count = forms.IntegerField(
        required=False,
        min_value=1,
        label='Goal Count',
        widget=StyledNumberInput(attrs={'placeholder': 'e.g. 5'})
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
        widgets = {
            'name': StyledTextInput(attrs={'placeholder': 'Habit name'}),
            'icon': StyledTextInput(attrs={'placeholder': 'e.g. 💧'}),
            'color': StyledTextInput(attrs={'type': 'color'}),
            'frequency': StyledSelect(),
            'category': StyledSelect(),
        }


class HabitLogForm(forms.ModelForm):
    note = forms.CharField(
        max_length=255,
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'Quick note...'}),
        label='Note (optional)'
    )

    class Meta:
        model = HabitLog
        fields = ['completion', 'note']
        widgets = {
            'completion': StyledSelect(),
        }