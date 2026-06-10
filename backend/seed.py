import os
import django
import random
from datetime import timedelta, date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innerlight.settings')
django.setup()

from faker import Faker
from django.utils import timezone
from accounts.models import CustomUser
from habittracker.models import Habit, HabitLog
from journal.models import JournalEntry, JournalPrompt
from moodtracker.models import MoodEntry
from mindfulness.models import BreathingSession, Affirmation
from notifications.models import NotificationSchedule, DoNotDisturb, NotificationLog
from progress.models import WeeklyReport, Achievement, UserAchievement, Streak

fake = Faker()

# ==========================================
# CONFIG — baguhin kung gusto mo
# ==========================================
NUM_USERS = 5
DAYS_OF_DATA = 30  # gaano karaming araw ng history


# ==========================================
# CLEAR EXISTING DATA
# ==========================================
def clear_data():
    print("🗑️  Clearing existing data...")
    UserAchievement.objects.all().delete()
    Achievement.objects.all().delete()
    WeeklyReport.objects.all().delete()
    Streak.objects.all().delete()
    NotificationLog.objects.all().delete()
    NotificationSchedule.objects.all().delete()
    DoNotDisturb.objects.all().delete()
    Affirmation.objects.filter(is_default=False).delete()
    BreathingSession.objects.all().delete()
    MoodEntry.objects.all().delete()
    JournalEntry.objects.all().delete()
    JournalPrompt.objects.all().delete()
    HabitLog.objects.all().delete()
    Habit.objects.all().delete()
    print("✅ Done clearing.\n")


# ==========================================
# USERS
# ==========================================
def seed_users():
    print("👤 Seeding users...")
    users = []
    intentions = [
        'Find calm within.',
        'Be present every day.',
        'Build better habits.',
        'Journal more often.',
        'Breathe and let go.',
    ]
    for i in range(NUM_USERS):
        username = fake.user_name() + str(random.randint(10, 99))
        user = CustomUser.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            display_name=fake.first_name(),
            personal_affirmation=fake.sentence(),
            wellness_intention=random.choice(intentions),
            theme=random.choice(['light', 'dark']),
            notif_morning_checkin=random.choice([True, False]),
            notif_journal_nudge=random.choice([True, False]),
            notif_streak_warning=random.choice([True, False]),
            notif_motivational=random.choice([True, False]),
            dnd_start=time(22, 0),
            dnd_end=time(7, 0),
            onboarding_complete=True,
            mood_baseline=random.randint(2, 4),
        )
        users.append(user)
        print(f"   Created user: {username}")
    print(f"✅ {NUM_USERS} users created.\n")
    return users


# ==========================================
# HABITS
# ==========================================
def seed_habits(users):
    print("✅ Seeding habits...")
    habit_data = [
        {'name': 'Morning Meditation', 'icon': '🧘', 'color': '#97A97C', 'category': 'mindfulness'},
        {'name': 'Drink 8 Glasses of Water', 'icon': '💧', 'color': '#6A9AB0', 'category': 'nutrition'},
        {'name': 'Evening Walk', 'icon': '🚶', 'color': '#B5C99A', 'category': 'movement'},
        {'name': 'Sleep by 10PM', 'icon': '🌙', 'color': '#9B8EC4', 'category': 'sleep'},
        {'name': 'Gratitude Journal', 'icon': '📓', 'color': '#C9A84C', 'category': 'mindfulness'},
        {'name': 'No Phone Before Bed', 'icon': '📵', 'color': '#D4A8A2', 'category': 'sleep'},
        {'name': 'Read 20 Minutes', 'icon': '📚', 'color': '#718355', 'category': 'mindfulness'},
        {'name': 'Stretch', 'icon': '🤸', 'color': '#E07B39', 'category': 'movement'},
    ]
    habits = []
    for user in users:
        selected = random.sample(habit_data, random.randint(3, 5))
        for h in selected:
            habit = Habit.objects.create(
                user=user,
                name=h['name'],
                icon=h['icon'],
                color=h['color'],
                category=h['category'],
                frequency=random.choice(['daily', 'weekdays', 'custom']),
                custom_days=random.sample(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 3),
                reminder_time=time(random.randint(6, 9), 0),
                goal_duration=random.choice([15, 20, 30, None]),
                goal_count=random.choice([1, 5, 8, None]),
            )
            habits.append(habit)

            # HabitLogs — last DAYS_OF_DATA days
            for i in range(DAYS_OF_DATA):
                log_date = date.today() - timedelta(days=i)
                HabitLog.objects.create(
                    habit=habit,
                    date=log_date,
                    completion=random.choice(['full', 'full', 'full', 'partial', 'skipped']),
                    note=fake.sentence() if random.random() > 0.7 else '',
                )
    print(f"✅ Habits and logs seeded.\n")
    return habits


# ==========================================
# MOOD ENTRIES
# ==========================================
def seed_moods(users):
    print("😊 Seeding mood entries...")
    emotion_tags = ['anxious', 'grateful', 'calm', 'sad', 'happy', 'angry', 'excited', 'tired']
    for user in users:
        for i in range(DAYS_OF_DATA):
            created = timezone.now() - timedelta(days=i)
            MoodEntry.objects.create(
                user=user,
                mood_score=random.randint(1, 5),
                energy_level=random.randint(1, 10),
                emotion_tag=random.choice(emotion_tags),
                note=fake.sentence() if random.random() > 0.5 else '',
                created_at=created,
            )
    print(f"✅ Mood entries seeded.\n")


# ==========================================
# JOURNAL ENTRIES
# ==========================================
def seed_journal(users):
    print("📓 Seeding journal entries...")
    prompts_data = [
        ('gratitude', 'What are three things you are grateful for today?'),
        ('gratitude', 'Who made your day better and why?'),
        ('reflection', 'What did you learn about yourself this week?'),
        ('reflection', 'What would you do differently today?'),
        ('growth', 'What is one habit you want to build this month?'),
        ('growth', 'What fear did you face recently?'),
        ('anxiety_release', 'What is weighing on your mind right now?'),
        ('anxiety_release', 'Write about something you cannot control and let it go.'),
    ]
    for category, text in prompts_data:
        JournalPrompt.objects.create(category=category, prompt_text=text)

    for user in users:
        for i in range(random.randint(10, DAYS_OF_DATA)):
            created = timezone.now() - timedelta(days=i)
            is_guided = random.random() > 0.5
            category, prompt = random.choice(prompts_data) if is_guided else ('', '')
            JournalEntry.objects.create(
                user=user,
                title=fake.sentence(nb_words=5) if random.random() > 0.4 else '',
                content=fake.paragraph(nb_sentences=random.randint(3, 8)),
                mood_score=random.randint(1, 5),
                tags=random.sample(['gratitude', 'work', 'family', 'growth', 'health'], random.randint(1, 3)),
                is_guided=is_guided,
                prompt_category=category,
                prompt_used=prompt,
                created_at=created,
            )
    print(f"✅ Journal entries seeded.\n")


# ==========================================
# BREATHING SESSIONS
# ==========================================
def seed_breathing(users):
    print("🌬️  Seeding breathing sessions...")
    types = ['box', '478', 'custom']
    for user in users:
        for i in range(random.randint(5, 15)):
            completed = timezone.now() - timedelta(days=random.randint(0, DAYS_OF_DATA))
            BreathingSession.objects.create(
                user=user,
                breathing_type=random.choice(types),
                inhale_duration=random.choice([4, 5, 6]),
                hold_duration=random.choice([4, 7, 0]),
                exhale_duration=random.choice([4, 8, 6]),
                duration_minutes=random.choice([5, 10, 15]),
                completed_at=completed,
            )
    print(f"✅ Breathing sessions seeded.\n")


# ==========================================
# AFFIRMATIONS
# ==========================================
def seed_affirmations():
    print("✨ Seeding affirmations...")
    default_affirmations = [
        'I am enough just as I am.',
        'I choose peace over worry.',
        'I am worthy of love and kindness.',
        'Every day I grow stronger.',
        'I trust the journey of my life.',
        'I am calm, centered, and grounded.',
        'I release what no longer serves me.',
        'My potential is limitless.',
        'I attract positivity and abundance.',
        'I am proud of how far I have come.',
    ]
    for text in default_affirmations:
        Affirmation.objects.get_or_create(
            text=text,
            defaults={'is_default': True, 'user': None}
        )
    print(f"✅ Affirmations seeded.\n")


# ==========================================
# NOTIFICATIONS
# ==========================================
def seed_notifications(users):
    print("🔔 Seeding notifications...")
    notif_types = ['morning_checkin', 'journal_nudge', 'streak_warning', 'motivational', 'habit_reminder']
    messages = {
        'morning_checkin': 'Good morning! How are you feeling today?',
        'journal_nudge': "Don't forget to write in your journal tonight.",
        'streak_warning': "Your streak is at risk! Log your habit today.",
        'motivational': 'You are doing amazing. Keep going!',
        'habit_reminder': "Time to work on your habit!",
    }
    for user in users:
        # Notification schedules
        for ntype in random.sample(notif_types, random.randint(2, 4)):
            NotificationSchedule.objects.create(
                user=user,
                notif_type=ntype,
                scheduled_time=time(random.randint(6, 21), 0),
                is_active=random.choice([True, True, False]),
            )

        # DND
        DoNotDisturb.objects.create(
            user=user,
            is_active=random.choice([True, False]),
            start_time=time(22, 0),
            end_time=time(7, 0),
        )

        # Notification logs
        for i in range(random.randint(5, 15)):
            ntype = random.choice(notif_types)
            NotificationLog.objects.create(
                user=user,
                notif_type=ntype,
                message=messages[ntype],
                sent_at=timezone.now() - timedelta(days=random.randint(0, DAYS_OF_DATA)),
                is_read=random.choice([True, False]),
            )
    print(f"✅ Notifications seeded.\n")


# ==========================================
# PROGRESS — ACHIEVEMENTS, REPORTS, STREAKS
# ==========================================
def seed_progress(users):
    print("📈 Seeding progress data...")

    # Achievements
    achievements_data = [
        ('7-Day Warrior', 'milestone_7', 'Logged habits for 7 days straight.', '🔥'),
        ('30-Day Champion', 'milestone_30', 'Logged habits for 30 days straight.', '🏆'),
        ('Journal Keeper', 'journaling', 'Wrote 10 journal entries.', '📓'),
        ('Calm Mind', 'calm_streak', 'Completed 5 breathing sessions.', '🧘'),
        ('Consistent Soul', 'consistency', 'Maintained a 14-day habit streak.', '⭐'),
    ]
    achievements = []
    for name, badge_type, desc, icon in achievements_data:
        a, _ = Achievement.objects.get_or_create(
            name=name,
            defaults={'badge_type': badge_type, 'description': desc, 'icon': icon}
        )
        achievements.append(a)

    for user in users:
        # Streak
        current = random.randint(0, 30)
        Streak.objects.create(
            user=user,
            current_streak=current,
            longest_streak=max(current, random.randint(current, 60)),
            last_checkin=date.today() - timedelta(days=random.randint(0, 2)),
        )

        # Weekly reports — last 4 weeks
        for w in range(4):
            week_start = date.today() - timedelta(weeks=w + 1)
            week_end = week_start + timedelta(days=6)
            WeeklyReport.objects.create(
                user=user,
                week_start=week_start,
                week_end=week_end,
                avg_mood_score=round(random.uniform(2.5, 4.8), 1),
                habit_completion_rate=round(random.uniform(40, 100), 1),
                best_streak=random.randint(3, 14),
                top_habit=random.choice(['Morning Meditation', 'Drink Water', 'Evening Walk', 'Read 20 Minutes']),
                reflection_prompt=fake.paragraph(nb_sentences=2),
            )

        # User achievements — random 1-3
        for achievement in random.sample(achievements, random.randint(1, 3)):
            UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'is_shared': random.choice([True, False])}
            )

    print(f"✅ Progress data seeded.\n")


# ==========================================
# RUN ALL
# ==========================================
if __name__ == '__main__':
    print("🌱 Starting InnerLight seed...\n")
    clear_data()
    
    superuser = CustomUser.objects.filter(is_superuser=True).first()
    if not superuser:
        print("❌ Walang superuser! Gumawa muna ng superuser gamit ang createsuperuser.")
        exit()
    
    print(f"👤 Using superuser: {superuser.username}\n")
    
    superuser.display_name = superuser.display_name or superuser.username
    superuser.wellness_intention = superuser.wellness_intention or 'Find calm within.'
    superuser.onboarding_complete = True
    superuser.save()
    
    users = [superuser]
    seed_habits(users)
    seed_moods(users)
    seed_journal(users)
    seed_breathing(users)
    seed_affirmations()
    seed_notifications(users)
    seed_progress(users)
    print("🎉 Seeding complete!")