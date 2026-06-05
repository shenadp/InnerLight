from django.db import models
from django.conf import settings

class MoodEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 5-point emoji scale
    MOOD_CHOICES = [
        (1, 'Awful'),
        (2, 'Bad'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Amazing'),
    ]
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    
    # Energy level slider
    energy_level = models.IntegerField()  # 1-10 (drained to energized)
    
    # Emotion tags
    EMOTION_TAGS = [
        ('anxious', 'Anxious'),
        ('grateful', 'Grateful'),
        ('calm', 'Calm'),
        ('sad', 'Sad'),
        ('happy', 'Happy'),
        ('angry', 'Angry'),
        ('excited', 'Excited'),
        ('tired', 'Tired'),
    ]
    emotion_tag = models.CharField(max_length=50, choices=EMOTION_TAGS, blank=True)
    
    # Optional mood note
    note = models.CharField(max_length=255, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_mood_score_display()} ({self.created_at})"