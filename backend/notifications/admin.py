from django.contrib import admin
from .models import NotificationSchedule, DoNotDisturb, NotificationLog

admin.site.register(NotificationSchedule)
admin.site.register(DoNotDisturb)
admin.site.register(NotificationLog)