from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NotificationSchedule, DoNotDisturb, NotificationLog
from .forms import NotificationScheduleForm, DoNotDisturbForm

@login_required
def notification_settings_view(request):
    schedules = NotificationSchedule.objects.filter(user=request.user)
    dnd, _ = DoNotDisturb.objects.get_or_create(
        user=request.user,
        defaults={'start_time': '22:00', 'end_time': '07:00'}
    )
    if request.method == 'POST':
        dnd_form = DoNotDisturbForm(request.POST, instance=dnd)
        if dnd_form.is_valid():
            dnd_form.save()
            messages.success(request, 'DND settings updated!')
            return redirect('notification_settings')
    else:
        dnd_form = DoNotDisturbForm(instance=dnd)
    context = {
        'schedules': schedules,
        'dnd_form': dnd_form,
    }
    return render(request, 'notifications/settings.html', context)

@login_required
def notification_create_view(request):
    if request.method == 'POST':
        form = NotificationScheduleForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.user = request.user
            notif.save()
            messages.success(request, 'Reminder created!')
            return redirect('notification_settings')
    else:
        form = NotificationScheduleForm()
    return render(request, 'notifications/create.html', {'form': form})

@login_required
def notification_delete_view(request, pk):
    schedule = get_object_or_404(NotificationSchedule, pk=pk, user=request.user)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Reminder deleted!')
        return redirect('notification_settings')
    return render(request, 'notifications/delete.html', {'schedule': schedule})

@login_required
def notification_log_view(request):
    logs = NotificationLog.objects.filter(user=request.user).order_by('-sent_at')
    return render(request, 'notifications/log.html', {'logs': logs})