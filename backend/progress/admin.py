from django.contrib import admin
from .models import WeeklyReport, Achievement, UserAchievement, Streak

admin.site.register(WeeklyReport)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Streak)