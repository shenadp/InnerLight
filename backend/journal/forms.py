from django import forms
from .models import JournalEntry
from accounts.widgets import ToggleWidget

class JournalEntryForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Title (optional)'}),
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your thoughts here...', 'rows': 10}),
        required=False,
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags (comma separated)'}),
        help_text='e.g. gratitude, work, family'
    )
    image = forms.ImageField(required=False, label='Attach Photo')
    voice_note = forms.FileField(required=False, label='Voice Note')
    prompt_category = forms.ChoiceField(
        choices=[('', '-- Select Prompt Category --')] + JournalEntry.PROMPT_CATEGORIES,
        required=False,
        label='Guided Prompt Category'
    )
    prompt_used = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Prompt used...', 'rows': 3}),
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