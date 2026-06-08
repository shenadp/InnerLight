from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from accounts.widgets import ToggleWidget, StyledTimeInput

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=100, required=False)
    wellness_intention = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'What do you want to feel?'})
    )
    mood_baseline = forms.IntegerField(
        min_value=1, 
        max_value=5, 
        required=False,
        help_text='Your current mood baseline (1-5)'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'display_name', 'wellness_intention', 'mood_baseline', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


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
            'biometric_lock',
            'private_mode',
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
            'notif_morning_checkin': ToggleWidget(),
            'notif_journal_nudge': ToggleWidget(),
            'notif_streak_warning': ToggleWidget(),
            'notif_motivational': ToggleWidget(),
            'dnd_start': StyledTimeInput(attrs={'type': 'time'}),
            'dnd_end': StyledTimeInput(attrs={'type': 'time'}),
            'biometric_lock': ToggleWidget(),
            'private_mode': ToggleWidget(),
        }