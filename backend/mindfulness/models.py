from django.db import models
from django.conf import settings

class BreathingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    BREATHING_TYPES = [
        ('box', 'Box Breathing (4-4-4-4)'),
        ('478', '4-7-8 Calming Breath'),
        ('custom', 'Custom'),
    ]
    breathing_type = models.CharField(max_length=20, choices=BREATHING_TYPES)
    
    # Custom inhale/hold/exhale timer
    inhale_duration = models.IntegerField(default=4)   # seconds
    hold_duration = models.IntegerField(default=4)
    exhale_duration = models.IntegerField(default=4)
    
    duration_minutes = models.IntegerField(default=5)  # total session length
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_breathing_type_display()}"


class AmbientSound(models.Model):
    SOUND_TYPES = [
        ('nature', 'Nature'),
        ('binaural', 'Binaural Tones'),
    ]
    name = models.CharField(max_length=100)
    sound_type = models.CharField(max_length=20, choices=SOUND_TYPES)
    
    BINAURAL_TYPES = [
        ('focus', 'Focus'),
        ('sleep', 'Sleep'),
        ('calm', 'Calm'),
    ]
    binaural_type = models.CharField(max_length=20, choices=BINAURAL_TYPES, blank=True)
    audio_file = models.FileField(upload_to='ambient_sounds/')

    def __str__(self):
        return self.name


class AmbientMixSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sounds = models.ManyToManyField(AmbientSound)  # up to 3 sounds
    sleep_timer_minutes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Ambient Mix"


class Affirmation(models.Model):
    text = models.TextField()
    is_default = models.BooleanField(default=True)  # False = custom by user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]