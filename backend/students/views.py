from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from jobs.models import JobCheck
from learning.models import Topic, ExamAttempt
from learning.utils import today_sessions, reminders
from resumes.models import ResumeVersion
from .models import StudentProfile


def home(request):
    return redirect('dashboard') if request.user.is_authenticated else render(request, 'home.html')


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        StudentProfile.objects.create(user=user)
        login(request, user)
        return redirect('upload')
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    u = request.user
    attempts = ExamAttempt.objects.filter(user=u)
    passed = attempts.filter(passed=True).order_by().values('topic').distinct().count()
    total = Topic.objects.count()
    chart = [{'label': a.topic.title, 'score': a.score} for a in reversed(list(attempts.select_related('topic')[:10]))]
    return render(request, 'dashboard.html', {
        'latest': ResumeVersion.objects.filter(user=u).first(), 'today': today_sessions(u),
        'reminders': reminders(u), 'jobs': JobCheck.objects.filter(user=u)[:4],
        'readiness': round(100 * passed / total) if total else 0, 'passed': passed, 'total': total,
        'chart': chart, 'goal': StudentProfile.objects.filter(user=u).values_list('career_goal', flat=True).first(), 'streak': attempts.dates('taken_at', 'day').count()})


@login_required
def history(request):
    u = request.user
    rid = request.GET.get('resume', '')
    jobs = JobCheck.objects.filter(user=u).select_related('resume')
    if rid.isdigit():
        jobs = jobs.filter(resume_id=rid)
    return render(request, 'history.html', {
        'resumes': ResumeVersion.objects.filter(user=u), 'jobs': jobs, 'rid': rid,
        'attempts': ExamAttempt.objects.filter(user=u).select_related('topic')})
