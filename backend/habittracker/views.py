from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit, HabitLog
from .forms import HabitForm, HabitLogForm
from django.utils import timezone

@login_required
def habit_list_view(request):
    habits = Habit.objects.filter(user=request.user).order_by('created_at')
    today = timezone.now().date()
    habit_status = []
    for habit in habits:
        log = HabitLog.objects.filter(habit=habit, date=today).first()
        habit_status.append({'habit': habit, 'log': log})
    return render(request, 'habittracker/list.html', {'habit_status': habit_status})

@login_required
def habit_create_view(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.custom_days = form.cleaned_data.get('custom_days', [])
            habit.save()
            messages.success(request, 'Habit created!')
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habittracker/create.html', {'form': form})

@login_required
def habit_edit_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habit updated!')
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habittracker/edit.html', {'form': form})

@login_required
def habit_delete_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Habit deleted!')
        return redirect('habit_list')
    return render(request, 'habittracker/delete.html', {'habit': habit})

@login_required
def habit_log_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    if request.method == 'POST':
        form = HabitLogForm(request.POST)
        if form.is_valid():
            log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
            log.completion = form.cleaned_data['completion']
            log.note = form.cleaned_data['note']
            log.save()
            messages.success(request, 'Habit logged!')
            return redirect('habit_list')
    else:
        form = HabitLogForm()
    return render(request, 'habittracker/log.html', {'form': form, 'habit': habit})

@login_required
def habit_heatmap_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    logs = HabitLog.objects.filter(habit=habit).order_by('date')
    return render(request, 'habittracker/heatmap.html', {'habit': habit, 'logs': logs})