from django import forms
from .models import JournalEntry
from accounts.widgets import (
    ToggleWidget, StyledTextInput, StyledTextarea,
    StyledSelect, StyledFileInput
)

class JournalEntryForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'Title (optional)'}),
    )
    content = forms.CharField(
        widget=StyledTextarea(attrs={'placeholder': 'Write your thoughts here...', 'rows': 10}),
        required=False,
    )
    tags = forms.CharField(
        required=False,
        widget=StyledTextInput(attrs={'placeholder': 'Add tags (comma separated)'}),
        help_text='e.g. gratitude, work, family'
    )
    image = forms.ImageField(
        required=False,
        label='Attach Photo',
        widget=StyledFileInput()
    )
    voice_note = forms.FileField(
        required=False,
        label='Voice Note',
        widget=StyledFileInput()
    )
    prompt_category = forms.ChoiceField(
        choices=[('', '-- Select Prompt Category --')] + JournalEntry.PROMPT_CATEGORIES,
        required=False,
        label='Guided Prompt Category',
        widget=StyledSelect()
    )
    prompt_used = forms.CharField(
        required=False,
        widget=StyledTextarea(attrs={'placeholder': 'Prompt used...', 'rows': 3}),
        label='Prompt'
    )
    is_guided = forms.BooleanField(
        required=False,
        label='Guided Entry?',
        widget=ToggleWidget()
    )

    class Meta:
        model = JournalEntry
        fields = [
            'title', 'content', 'image', 'voice_note',
            'tags', 'prompt_category', 'prompt_used', 'is_guided',
        ]