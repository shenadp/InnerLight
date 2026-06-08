from django import forms
from .models import BreathingSession, Affirmation
from accounts.widgets import ToggleWidget

class BreathingSessionForm(forms.ModelForm):
    inhale_duration = forms.IntegerField(min_value=1, max_value=20, initial=4, label='Inhale Duration (seconds)')
    hold_duration = forms.IntegerField(min_value=0, max_value=20, initial=4, label='Hold Duration (seconds)')
    exhale_duration = forms.IntegerField(min_value=1, max_value=20, initial=4, label='Exhale Duration (seconds)')
    duration_minutes = forms.IntegerField(min_value=1, max_value=60, initial=5, label='Total Session Length (minutes)')

    class Meta:
        model = BreathingSession
        fields = ['breathing_type', 'inhale_duration', 'hold_duration', 'exhale_duration', 'duration_minutes']


class AffirmationForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your affirmation...', 'rows': 3}),
        label='Affirmation'
    )
    is_favorite = forms.BooleanField(
        required=False,
        label='Add to Favorites',
        widget=ToggleWidget()
    )

    class Meta:
        model = Affirmation
        fields = ['text', 'is_favorite']