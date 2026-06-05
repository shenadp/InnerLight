from django.db import models
from django.conf import settings

class NotificationSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    NOTIF_TYPES = [
        ('morning_checkin', 'Morning Check-in'),
        ('journal_nudge', 'Evening Journal Nudge'),
        ('streak_warning', 'Streak At-risk Warning'),
        ('motivational', 'Motivational Quote'),
        ('habit_reminder', 'Habit Reminder'),
    ]
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    scheduled_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_notif_type_display()} at {self.scheduled_time}"


class DoNotDisturb(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - DND {self.start_time} to {self.end_time}"


class NotificationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notif_type = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.notif_type} - {self.sent_at}"