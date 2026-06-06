from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from accounts.models import CustomUser
from moodtracker.models import MoodEntry
from habittracker.models import Habit, HabitLog
from journal.models import JournalEntry, JournalPrompt
from mindfulness.models import BreathingSession, AmbientSound, Affirmation
from progress.models import WeeklyReport, Achievement, UserAchievement, Streak
from notifications.models import NotificationSchedule, DoNotDisturb, NotificationLog

from .serializers import (
    UserSerializer, MoodEntrySerializer, HabitSerializer, HabitLogSerializer,
    JournalEntrySerializer, JournalPromptSerializer, BreathingSessionSerializer,
    AmbientSoundSerializer, AffirmationSerializer, WeeklyReportSerializer,
    AchievementSerializer, UserAchievementSerializer, StreakSerializer,
    NotificationScheduleSerializer, DoNotDisturbSerializer, NotificationLogSerializer
)


# ==========================================
# AUTH
# ==========================================

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                password=request.data.get('password'),
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ==========================================
# USER / PROFILE
# ==========================================

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ==========================================
# MOOD TRACKER
# ==========================================

class MoodEntryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MoodEntryDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class MoodInsightsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_7 = today - timedelta(days=7)
        last_30 = today - timedelta(days=30)

        entries_7 = MoodEntry.objects.filter(user=request.user, created_at__date__gte=last_7)
        entries_30 = MoodEntry.objects.filter(user=request.user, created_at__date__gte=last_30)

        from collections import Counter
        emotion_counts = Counter(e.emotion_tag for e in entries_30 if e.emotion_tag)

        return Response({
            'entries_7': MoodEntrySerializer(entries_7, many=True).data,
            'entries_30': MoodEntrySerializer(entries_30, many=True).data,
            'top_emotions': emotion_counts.most_common(5),
            'best_mood': MoodEntrySerializer(entries_30.order_by('-mood_score').first()).data if entries_30.exists() else None,
            'lowest_mood': MoodEntrySerializer(entries_30.order_by('mood_score').first()).data if entries_30.exists() else None,
        })


# ==========================================
# HABIT TRACKER
# ==========================================

class HabitListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitLogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(habit__user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save()


# ==========================================
# JOURNAL
# ==========================================

class JournalEntryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JournalEntry.objects.filter(user=self.request.user).order_by('-created_at')
        query = self.request.query_params.get('q')
        tag = self.request.query_params.get('tag')
        if query:
            queryset = queryset.filter(content__icontains=query)
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JournalEntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


class JournalPromptListAPIView(generics.ListAPIView):
    serializer_class = JournalPromptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        queryset = JournalPrompt.objects.all()
        if category:
            queryset = queryset.filter(category=category)
        return queryset


# ==========================================
# MINDFULNESS
# ==========================================

class BreathingSessionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BreathingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BreathingSession.objects.filter(user=self.request.user).order_by('-completed_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AmbientSoundListAPIView(generics.ListAPIView):
    serializer_class = AmbientSoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sound_type = self.request.query_params.get('type')
        queryset = AmbientSound.objects.all()
        if sound_type:
            queryset = queryset.filter(sound_type=sound_type)
        return queryset


class AffirmationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AffirmationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Affirmation.objects.filter(
            user=self.request.user
        ) | Affirmation.objects.filter(is_default=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_default=False)


# ==========================================
# PROGRESS
# ==========================================

class WeeklyReportListAPIView(generics.ListAPIView):
    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeeklyReport.objects.filter(user=self.request.user).order_by('-week_start')


class AchievementListAPIView(generics.ListAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Achievement.objects.all()


class UserAchievementListAPIView(generics.ListAPIView):
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user).order_by('-unlocked_at')


class StreakAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StreakSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        streak, _ = Streak.objects.get_or_create(user=self.request.user)
        return streak


# ==========================================
# NOTIFICATIONS
# ==========================================

class NotificationScheduleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = NotificationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationSchedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationSchedule.objects.filter(user=self.request.user)


class DoNotDisturbAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DoNotDisturbSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        dnd, _ = DoNotDisturb.objects.get_or_create(
            user=self.request.user,
            defaults={'start_time': '22:00', 'end_time': '07:00'}
        )
        return dnd


class NotificationLogListAPIView(generics.ListAPIView):
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationLog.objects.filter(user=self.request.user).order_by('-sent_at')
    
from .external import get_daily_affirmation, get_quote_of_day

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def daily_content(request):
    return Response({
        'affirmation': get_daily_affirmation(),
        'quote': get_quote_of_day(),
    })