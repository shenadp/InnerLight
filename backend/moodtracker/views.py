from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MoodEntry
from .forms import MoodEntryForm
from django.utils import timezone
from datetime import timedelta

@login_required
def mood_checkin_view(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged successfully!')
            return redirect('mood_insights')
    else:
        form = MoodEntryForm()
    return render(request, 'moodtracker/checkin.html', {'form': form})


@login_required
def mood_insights_view(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    entries_7 = MoodEntry.objects.filter(
        user=request.user,
        created_at__date__gte=last_7_days
    ).order_by('created_at')

    entries_30 = MoodEntry.objects.filter(
        user=request.user,
        created_at__date__gte=last_30_days
    ).order_by('created_at')

    # Top recurring emotions
    from collections import Counter
    emotion_counts = Counter(
        e.emotion_tag for e in entries_30 if e.emotion_tag
    )
    top_emotions = emotion_counts.most_common(5)

    # Best & lowest mood day
    best_mood = entries_30.order_by('-mood_score').first()
    lowest_mood = entries_30.order_by('mood_score').first()

    context = {
        'entries_7': entries_7,
        'entries_30': entries_30,
        'top_emotions': top_emotions,
        'best_mood': best_mood,
        'lowest_mood': lowest_mood,
    }
    return render(request, 'moodtracker/insights.html', context)


@login_required
def mood_history_view(request):
    entries = MoodEntry.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'moodtracker/history.html', {'entries': entries})