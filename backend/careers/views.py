from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from students.models import StudentProfile
from .catalog import CATEGORIES, CATEGORY_OF, EMERGING
from resumes.models import ResumeVersion
from learning.models import ExamAttempt
from .models import CareerPath
from .scoring import score_resume


@login_required
def results(request, pk):
    rv = get_object_or_404(ResumeVersion, pk=pk, user=request.user)
    return render(request, 'career_results.html', {
        'rv': rv, 'results': score_resume(rv.skills), 'few': len(rv.skills) < 3})


@login_required
def career_detail(request, slug):
    career = get_object_or_404(CareerPath, slug=slug, active=True)
    rv = None
    if request.GET.get('resume', '').isdigit():
        rv = ResumeVersion.objects.filter(pk=request.GET['resume'], user=request.user).first()
    passed = set(ExamAttempt.objects.filter(user=request.user, passed=True).values_list('topic_id', flat=True))
    rows, prev, current_set = [], None, False
    for t in career.topics.order_by('order').prefetch_related('questions'):
        if t.pk in passed:
            state = 'passed'
        elif not current_set:
            state, current_set = 'current', True
        else:
            state = 'fog'
        rows.append({'t': t, 'state': state, 'has_exam': t.questions.exists(),
                     'prev_missing': prev.title if prev and prev.pk not in passed else None})
        prev = t
    have = {s.lower() for s in rv.skills} if rv else set()
    skills = [(s.skill, s.skill in have) for s in career.skills.all()] if rv else []
    done = sum(1 for r in rows if r['state'] == 'passed')
    return render(request, 'career_detail.html', {
        'career': career, 'rows': rows, 'rv': rv, 'skills': skills,
        'progress': round(100 * done / len(rows)) if rows else 0})


@login_required
def explore(request):
    """Browse every role, filter by field or 'new', and (with a resume) see the estimated fit for each."""
    q, cat = request.GET.get('q', '').strip().lower(), request.GET.get('cat', '')
    mine = ResumeVersion.objects.filter(user=request.user, status='complete')
    rid = request.GET.get('resume', '')
    rv = mine.filter(pk=rid).first() if rid.isdigit() else mine.first()
    scores = {r['career'].pk: r for r in score_resume(rv.skills, limit=None)} if rv else {}
    roles = []
    for c in CareerPath.objects.filter(active=True):
        category, new = CATEGORY_OF.get(c.title, 'Other'), c.title in EMERGING
        if cat == 'new' and not new or cat not in ('', 'new') and category != cat:
            continue
        if q and q not in c.title.lower() and q not in c.description.lower():
            continue
        r = scores.get(c.pk)
        roles.append({'c': c, 'category': category, 'new': new, 'score': r['score'] if r else None,
                      'missing': r['missing'][:3] if r else []})
    roles.sort(key=lambda r: (-(r['score'] if r['score'] is not None else -1), r['category'], r['c'].title))
    goal = StudentProfile.objects.get_or_create(user=request.user)[0].career_goal
    return render(request, 'explore.html', {'roles': roles, 'categories': CATEGORIES, 'cat': cat, 'q': q,
                                            'rv': rv, 'resumes': mine, 'goal': goal})


@login_required
@require_POST
def set_goal(request, slug):
    career = get_object_or_404(CareerPath, slug=slug, active=True)
    p, _ = StudentProfile.objects.get_or_create(user=request.user)
    p.career_goal = career.title
    p.save()
    messages.success(request, f'Goal set: {career.title}. Follow its trail from the role page.')
    return redirect('career_detail', slug=slug)
