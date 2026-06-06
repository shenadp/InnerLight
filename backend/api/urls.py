from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [

    # AUTH
    path('auth/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

    # PROFILE
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),

    # MOOD
    path('mood/', views.MoodEntryListCreateAPIView.as_view(), name='api_mood_list'),
    path('mood/<int:pk>/', views.MoodEntryDetailAPIView.as_view(), name='api_mood_detail'),
    path('mood/insights/', views.MoodInsightsAPIView.as_view(), name='api_mood_insights'),

    # HABITS
    path('habits/', views.HabitListCreateAPIView.as_view(), name='api_habit_list'),
    path('habits/<int:pk>/', views.HabitDetailAPIView.as_view(), name='api_habit_detail'),
    path('habits/logs/', views.HabitLogListCreateAPIView.as_view(), name='api_habit_logs'),

    # JOURNAL
    path('journal/', views.JournalEntryListCreateAPIView.as_view(), name='api_journal_list'),
    path('journal/<int:pk>/', views.JournalEntryDetailAPIView.as_view(), name='api_journal_detail'),
    path('journal/prompts/', views.JournalPromptListAPIView.as_view(), name='api_journal_prompts'),

    # MINDFULNESS
    path('breathing/', views.BreathingSessionListCreateAPIView.as_view(), name='api_breathing_list'),
    path('sounds/', views.AmbientSoundListAPIView.as_view(), name='api_sounds_list'),
    path('affirmations/', views.AffirmationListCreateAPIView.as_view(), name='api_affirmations_list'),

    # PROGRESS
    path('progress/reports/', views.WeeklyReportListAPIView.as_view(), name='api_reports_list'),
    path('progress/achievements/', views.AchievementListAPIView.as_view(), name='api_achievements_list'),
    path('progress/my-achievements/', views.UserAchievementListAPIView.as_view(), name='api_user_achievements'),
    path('progress/streak/', views.StreakAPIView.as_view(), name='api_streak'),

    # NOTIFICATIONS
    path('notifications/', views.NotificationScheduleListCreateAPIView.as_view(), name='api_notif_list'),
    path('notifications/<int:pk>/', views.NotificationScheduleDetailAPIView.as_view(), name='api_notif_detail'),
    path('notifications/dnd/', views.DoNotDisturbAPIView.as_view(), name='api_dnd'),
    path('notifications/log/', views.NotificationLogListAPIView.as_view(), name='api_notif_log'),
]