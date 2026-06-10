from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from accounts.widgets import (
    ToggleWidget, StyledTimeInput, StyledTextInput, 
    StyledTextarea, StyledNumberInput, StyledSelect, StyledFileInput
)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=StyledTextInput(attrs={'placeholder': 'Email address'})
    )
    display_name = forms.CharField(
        max_length=100,
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'Display Name'})
    )
    wellness_intention = forms.CharField(
        max_length=255,
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'What do you want to feel?'})
    )
    mood_baseline = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=False,
        help_text='Your current mood baseline (1-5)',
        widget=StyledNumberInput(attrs={'placeholder': '1-5'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'display_name', 'wellness_intention', 'mood_baseline', 'password1', 'password2']
        widgets = {
            'username': StyledTextInput(attrs={'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=StyledTextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'display_name',
            'avatar',
            'personal_affirmation',
            'wellness_intention',
            'theme',
            'notif_morning_checkin',
            'notif_journal_nudge',
            'notif_streak_warning',
            'notif_motivational',
            'dnd_start',
            'dnd_end',
        ]
        labels = {
            'display_name': 'Display Name',
            'avatar': 'Profile Photo',
            'personal_affirmation': 'Personal Affirmation',
            'wellness_intention': 'Wellness Intention',
            'theme': 'Theme',
            'notif_morning_checkin': 'Morning Check-in',
            'notif_journal_nudge': 'Journal Reminder',
            'notif_streak_warning': 'Streak Warning',
            'notif_motivational': 'Motivational Quotes',
            'dnd_start': 'Do Not Disturb — Start',
            'dnd_end': 'Do Not Disturb — End',
            'biometric_lock': 'Biometric Lock',
            'private_mode': 'Private Mode',
        }
        widgets = {
            'display_name': StyledTextInput(attrs={'placeholder': 'Your display name'}),
            'personal_affirmation': StyledTextarea(attrs={'placeholder': 'Write your personal affirmation...', 'rows': 3}),
            'wellness_intention': StyledTextInput(attrs={'placeholder': 'What do you want to feel?'}),
            'theme': StyledSelect(),
            'avatar': StyledFileInput(),
            'notif_morning_checkin': ToggleWidget(),
            'notif_journal_nudge': ToggleWidget(),
            'notif_streak_warning': ToggleWidget(),
            'notif_motivational': ToggleWidget(),
            'dnd_start': StyledTimeInput(attrs={'type': 'time'}),
            'dnd_end': StyledTimeInput(attrs={'type': 'time'}),
        }