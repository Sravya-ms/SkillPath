import datetime, random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import SessionForm
from .models import Topic, ExamQuestion, ExamAttempt, StudySession
from .utils import today_sessions, reminders

PASS_PERCENT = 75
EXAM_SIZE = 10


@login_required
def exam(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    key = f'exam_{topic.pk}'
    if request.method == 'POST':
        ids = request.session.pop(key, None)
        if not ids:
            return redirect('exam', topic_id=topic.pk)
        qs = list(ExamQuestion.objects.filter(pk__in=ids))
        right = sum(1 for q in qs if request.POST.get(f'q{q.pk}') == str(q.correct))
        passed = right * 100 >= PASS_PERCENT * len(qs)          # integer maths: 3/4 = 75% passes
        score = round(100 * right / len(qs))
        n = ExamAttempt.objects.filter(user=request.user, topic=topic).count() + 1
        ExamAttempt.objects.create(user=request.user, topic=topic, score=score, passed=passed, attempt_no=n)
        return render(request, 'exam_result.html', {'topic': topic, 'score': score, 'passed': passed,
                                                    'right': right, 'total': len(qs), 'attempt': n})
    pool = list(topic.questions.all())
    if not pool:
        messages.info(request, 'No questions for this topic yet - an admin needs to add some.')
        return redirect('dashboard')
    chosen = random.sample(pool, min(EXAM_SIZE, len(pool)))
    request.session[key] = [q.pk for q in chosen]
    items = []
    for q in chosen:
        opts = list(enumerate(q.options))
        random.shuffle(opts)
        items.append({'q': q, 'opts': opts})
    return render(request, 'exam.html', {'topic': topic, 'items': items})


@login_required
def planner(request):
    form = SessionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        s = form.save(commit=False)
        s.user = request.user
        s.save()
        messages.success(request, 'Session added.')
        return redirect('planner')
    today = timezone.localdate()
    monday = today - datetime.timedelta(days=today.weekday())
    mine = list(StudySession.objects.filter(user=request.user).select_related('topic'))
    week = []
    for i in range(7):
        d = monday + datetime.timedelta(days=i)
        week.append({'date': d, 'is_today': d == today, 'items': [(s, s.state_on(d)) for s in mine if s.occurs_on(d)]})
    return render(request, 'planner.html', {'form': form, 'week': week, 'today': today_sessions(request.user),
                                            'sessions': mine, 'reminders': reminders(request.user)})


@login_required
@require_POST
def session_action(request, pk, action):
    s = get_object_or_404(StudySession, pk=pk, user=request.user)
    today = timezone.localdate()
    if action == 'done':
        s.last_done, s.last_missed = today, None
    elif action == 'missed':
        s.last_missed, s.last_done = today, None
    elif action == 'pause':
        s.paused = not s.paused
    elif action == 'delete':
        s.delete()
        return redirect('planner')
    s.save()
    return redirect('planner')
