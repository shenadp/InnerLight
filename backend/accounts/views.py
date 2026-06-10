from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserProfileForm
from .utils import get_daily_quote
from django.http import JsonResponse
import json

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.display_name or user.username}!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('account_login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'account/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    from progress.models import Streak
    from moodtracker.models import MoodEntry
    from habittracker.models import Habit, HabitLog
    from datetime import date

    quote = get_daily_quote()

    streak = Streak.objects.filter(user=request.user).first()

    today_mood = MoodEntry.objects.filter(
        user=request.user,
        created_at__date=date.today()
    ).last()

    habit_status = []
    habits = Habit.objects.filter(user=request.user)
    for habit in habits:
        log = HabitLog.objects.filter(habit=habit, date=date.today()).first()
        habit_status.append({'habit': habit, 'log': log})

    return render(request, 'dashboard.html', {
        'user': request.user,
        'quote': quote,
        'streak': streak,
        'today_mood': today_mood,
        'habit_status': habit_status, 
    })

@login_required
def set_theme_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme')
        if theme in ['light', 'dark']:
            request.user.theme = theme
            request.user.save(update_fields=['theme'])
    return JsonResponse({'status': 'ok'})