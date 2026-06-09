from django import forms
from .models import MoodEntry
from accounts.widgets import StyledTextInput, StyledSelect

class MoodEntryForm(forms.ModelForm):
    mood_score = forms.ChoiceField(
        choices=MoodEntry.MOOD_CHOICES,
        widget=forms.RadioSelect,
        label='How are you feeling?'
    )
    energy_level = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': 1,
            'max': 10,
            'class': 'il-range'
        }),
        label='Energy Level (Drained → Energized)'
    )
    emotion_tag = forms.ChoiceField(
        choices=[('', '-- Select Emotion --')] + MoodEntry.EMOTION_TAGS,
        required=False,
        label='How would you describe it?',
        widget=StyledSelect()
    )
    note = forms.CharField(
        max_length=255,
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'Add a quick note...'}),
        label='Mood Note (optional)'
    )

    class Meta:
        model = MoodEntry
        fields = ['mood_score', 'energy_level', 'emotion_tag', 'note']