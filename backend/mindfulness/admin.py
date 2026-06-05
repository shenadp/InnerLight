from django.contrib import admin
from .models import BreathingSession, AmbientSound, AmbientMixSession, Affirmation

admin.site.register(BreathingSession)
admin.site.register(AmbientSound)
admin.site.register(AmbientMixSession)
admin.site.register(Affirmation)