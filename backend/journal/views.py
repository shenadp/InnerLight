from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalEntry, JournalPrompt
from .forms import JournalEntryForm
import random

@login_required
def journal_list_view(request):
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    if query:
        entries = entries.filter(
            content__icontains=query
        ) | entries.filter(
            title__icontains=query
        )
        entries = entries.filter(user=request.user).order_by('-created_at')

    if tag:
        entries = entries.filter(tags__icontains=tag.lower().strip())

    # Kuhanin lahat ng unique tags ng user
    all_entries = JournalEntry.objects.filter(user=request.user)
    all_tags = set()
    for entry in all_entries:
        if entry.tags:
            for t in entry.tags:
                all_tags.add(t)
    all_tags = sorted(all_tags)

    return render(request, 'journal/list.html', {
        'entries': entries,
        'query': query,
        'tag': tag,
        'all_tags': all_tags,
    })

@login_required
def journal_create_view(request):
    prompt = None
    category = request.GET.get('category', '')
    if category:
        prompts = JournalPrompt.objects.filter(category=category)
        if prompts.exists():
            prompt = random.choice(prompts)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.mood_score = request.user.mood_baseline
            tags_input = form.cleaned_data.get('tags', '')
            entry.tags = [t.strip() for t in tags_input.split(',') if t.strip()]
            entry.save()
            messages.success(request, 'Journal entry saved!')
            return redirect('journal_list')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/create.html', {'form': form, 'prompt': prompt})

@login_required
def journal_detail_view(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    return render(request, 'journal/detail.html', {'entry': entry})

@login_required
def journal_edit_view(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Journal entry updated!')
            return redirect('journal_detail', pk=pk)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'journal/edit.html', {'form': form, 'entry': entry})

@login_required
def journal_delete_view(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Journal entry deleted!')
        return redirect('journal_list')
    return render(request, 'journal/delete.html', {'entry': entry})