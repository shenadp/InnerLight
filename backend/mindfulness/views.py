from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BreathingSession, AmbientSound, Affirmation
from .forms import BreathingSessionForm, AffirmationForm
from accounts.utils import get_daily_quote
import random

@login_required
def calm_view(request):
    recent_session = BreathingSession.objects.filter(user=request.user).order_by('completed_at').first()
    return render(request, 'mindfulness/calmness.html', {'recent_session': recent_session})

@login_required
def breathing_view(request):
    if request.method == 'POST':
        form = BreathingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, 'Breathing session logged!')
            return redirect('breathing')
    else:
        form = BreathingSessionForm()
    return render(request, 'mindfulness/breathing.html', {'form': form})

@login_required
def ambient_view(request):
    nature_sounds = AmbientSound.objects.filter(sound_type='nature')
    binaural_sounds = AmbientSound.objects.filter(sound_type='binaural')
    context = {
        'nature_sounds': nature_sounds,
        'binaural_sounds': binaural_sounds,
    }
    return render(request, 'mindfulness/ambient.html', context)

@login_required
def affirmation_view(request):
    daily = get_daily_quote()
    user_affirmations = Affirmation.objects.filter(user=request.user)
    favorites = user_affirmations.filter(is_favorite=True)

    if request.method == 'POST':
        form = AffirmationForm(request.POST)
        if form.is_valid():
            affirmation = form.save(commit=False)
            affirmation.user = request.user
            affirmation.is_default = False
            affirmation.save()
            messages.success(request, 'Affirmation added!')
            return redirect('affirmation')
    else:
        form = AffirmationForm()

    context = {
        'daily': daily,
        'user_affirmations': user_affirmations,
        'favorites': favorites,
        'form': form,
    }
    return render(request, 'mindfulness/affirmation.html', context)