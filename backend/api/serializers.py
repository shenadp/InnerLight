from rest_framework import serializers
from accounts.models import CustomUser
from moodtracker.models import MoodEntry
from habittracker.models import Habit, HabitLog
from journal.models import JournalEntry, JournalPrompt
from mindfulness.models import BreathingSession, AmbientSound, Affirmation
from progress.models import WeeklyReport, Achievement, UserAchievement, Streak
from notifications.models import NotificationSchedule, DoNotDisturb, NotificationLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'display_name', 'avatar',
                  'personal_affirmation', 'wellness_intention', 'theme',
                  'onboarding_complete', 'mood_baseline']
        read_only_fields = ['id']


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['id', 'mood_score', 'energy_level', 'emotion_tag', 'note', 'created_at']
        read_only_fields = ['id', 'created_at']


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'icon', 'color', 'frequency', 'custom_days',
                  'category', 'reminder_time', 'goal_duration', 'goal_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'date', 'completion', 'note', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'mood_score', 'image', 'voice_note',
                  'tags', 'prompt_category', 'prompt_used', 'is_guided',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class JournalPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalPrompt
        fields = ['id', 'category', 'prompt_text', 'is_seasonal', 'season_theme']
        read_only_fields = ['id']


class BreathingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathingSession
        fields = ['id', 'breathing_type', 'inhale_duration', 'hold_duration',
                  'exhale_duration', 'duration_minutes', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class AmbientSoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbientSound
        fields = ['id', 'name', 'sound_type', 'binaural_type', 'audio_file']
        read_only_fields = ['id']


class AffirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affirmation
        fields = ['id', 'text', 'is_default', 'is_favorite']
        read_only_fields = ['id']


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = ['id', 'week_start', 'week_end', 'avg_mood_score',
                  'habit_completion_rate', 'best_streak', 'top_habit',
                  'reflection_prompt', 'generated_at']
        read_only_fields = ['id', 'generated_at']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'badge_type', 'description', 'icon']
        read_only_fields = ['id']


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'unlocked_at', 'is_shared']
        read_only_fields = ['id', 'unlocked_at']


class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = ['id', 'current_streak', 'longest_streak', 'last_checkin']
        read_only_fields = ['id']


class NotificationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSchedule
        fields = ['id', 'notif_type', 'scheduled_time', 'is_active']
        read_only_fields = ['id']


class DoNotDisturbSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoNotDisturb
        fields = ['id', 'is_active', 'start_time', 'end_time']
        read_only_fields = ['id']


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ['id', 'notif_type', 'message', 'sent_at', 'is_read']
        read_only_fields = ['id', 'sent_at']