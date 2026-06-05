from django.db import models
from django.conf import settings

class WeeklyReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField()
    week_end = models.DateField()
    
    # Auto-generated stats
    avg_mood_score = models.FloatField(null=True, blank=True)
    habit_completion_rate = models.FloatField(null=True, blank=True)  # percentage
    best_streak = models.IntegerField(default=0)
    top_habit = models.CharField(max_length=100, blank=True)
    reflection_prompt = models.TextField(blank=True)
    
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"


class Achievement(models.Model):
    BADGE_TYPES = [
        ('consistency', 'Consistency'),
        ('journaling', 'Journaling'),
        ('calm_streak', 'Calm Streak'),
        ('milestone_7', '7-Day Milestone'),
        ('milestone_30', '30-Day Milestone'),
        ('milestone_100', '100-Day Milestone'),
    ]
    name = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # emoji or icon name

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    is_shared = models.BooleanField(default=False)  # shareable achievement cards

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class Streak(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_checkin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"