from django.db import models
from django.conf import settings

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)  # emoji or icon name
    color = models.CharField(max_length=7, blank=True)  # hex color e.g. #7F77DD

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekdays', 'Weekdays'),
        ('custom', 'Custom Days'),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    custom_days = models.JSONField(default=list, blank=True)  # e.g. ['Mon', 'Wed', 'Fri']

    CATEGORY_CHOICES = [
        ('sleep', 'Sleep'),
        ('movement', 'Movement'),
        ('mindfulness', 'Mindfulness'),
        ('nutrition', 'Nutrition'),
        ('social', 'Social'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    
    reminder_time = models.TimeField(null=True, blank=True)
    goal_duration = models.IntegerField(null=True, blank=True)  # in minutes
    goal_count = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    
    COMPLETION_CHOICES = [
        ('full', 'Full'),
        ('partial', 'Partial'),
        ('skipped', 'Skipped'),
    ]
    completion = models.CharField(max_length=10, choices=COMPLETION_CHOICES, default='full')
    note = models.CharField(max_length=255, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.completion}"