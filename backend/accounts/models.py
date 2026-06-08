from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True)
    personal_affirmation = models.TextField(blank=True)
    wellness_intention = models.CharField(max_length=255, blank=True)

    # THEME PREFERENCES
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')

    # NOTIFICATION PREFERENCES
    notif_morning_checkin = models.BooleanField(default=True)
    notif_journal_nudge = models.BooleanField(default=True)
    notif_streak_warning = models.BooleanField(default=True)
    notif_motivational = models.BooleanField(default=True)
    dnd_start = models.TimeField(null=True, blank=True)
    dnd_end = models.TimeField(null=True, blank=True)

    # PRIVACY
    biometric_lock = models.BooleanField(default=False)
    private_mode = models.BooleanField(default=False)

    # ONBOARDING
    onboarding_complete = models.BooleanField(default=False)
    mood_baseline = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
