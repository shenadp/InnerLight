from django import forms
from .models import WeeklyReport, UserAchievement

class WeeklyReportForm(forms.ModelForm):
    week_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Week Start'
    )
    week_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Week End'
    )
    reflection_prompt = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Your reflection for the week...', 'rows': 4}),
        label='Reflection'
    )

    class Meta:
        model = WeeklyReport
        fields = [
            'week_start',
            'week_end',
            'reflection_prompt',
        ]


class ShareAchievementForm(forms.ModelForm):
    is_shared = forms.BooleanField(
        required=False,
        label='Share this Achievement'
    )

    class Meta:
        model = UserAchievement
        fields = ['is_shared']