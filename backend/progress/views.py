from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WeeklyReport, Achievement, UserAchievement, Streak
from .forms import WeeklyReportForm, ShareAchievementForm
from django.utils import timezone

@login_required
def progress_view(request):
    streak, _ = Streak.objects.get_or_create(user=request.user)
    achievements = UserAchievement.objects.filter(user=request.user).order_by('-unlocked_at')
    latest_report = WeeklyReport.objects.filter(user=request.user).order_by('-week_start').first()
    context = {
        'streak': streak,
        'achievements': achievements,
        'latest_report': latest_report,
    }
    return render(request, 'progress/progress.html', context)

@login_required
def weekly_report_view(request):
    reports = WeeklyReport.objects.filter(user=request.user).order_by('-week_start')
    return render(request, 'progress/weekly_report.html', {'reports': reports})

@login_required
def achievements_view(request):
    all_achievements = Achievement.objects.all()
    unlocked = UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
    context = {
        'all_achievements': all_achievements,
        'unlocked': unlocked,
    }
    return render(request, 'progress/achievements.html', context)

@login_required
def share_achievement_view(request, pk):
    user_achievement = get_object_or_404(UserAchievement, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShareAchievementForm(request.POST, instance=user_achievement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement sharing updated!')
            return redirect('achievements')
    else:
        form = ShareAchievementForm(instance=user_achievement)
    return render(request, 'progress/share.html', {'form': form, 'ua': user_achievement})