from django.contrib import admin
from .models import JournalEntry, JournalPrompt

admin.site.register(JournalEntry)
admin.site.register(JournalPrompt)