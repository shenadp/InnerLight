from django.db import models
from django.conf import settings

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Free journal
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)  # rich text (bold, italic, lists)
    
    # Mood & date auto-attached
    mood_score = models.IntegerField(null=True, blank=True)  # 1-5
    
    # Photo/image attachment
    image = models.ImageField(upload_to='journal_images/', blank=True, null=True)
    
    # Voice-to-text
    voice_note = models.FileField(upload_to='journal_voice/', blank=True, null=True)
    
    # Tags
    tags = models.JSONField(default=list, blank=True)  # e.g. ['gratitude', 'work']
    
    # Guided prompt
    PROMPT_CATEGORIES = [
        ('gratitude', 'Gratitude'),
        ('reflection', 'Reflection'),
        ('growth', 'Growth'),
        ('anxiety_release', 'Anxiety Release'),
    ]
    prompt_category = models.CharField(max_length=20, choices=PROMPT_CATEGORIES, blank=True)
    prompt_used = models.TextField(blank=True)  # the actual prompt text
    
    is_guided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"


class JournalPrompt(models.Model):
    category = models.CharField(max_length=20)
    prompt_text = models.TextField()
    is_seasonal = models.BooleanField(default=False)
    season_theme = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.category} - {self.prompt_text[:50]}"