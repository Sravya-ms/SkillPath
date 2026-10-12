import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from careers.skills import extract_skills
from learning.models import Topic
from resumes.models import ResumeVersion
from .fetch import fetch_job_text, FetchError
from .models import JobCheck, PlanTask


@login_required
def check(request):
    resumes = ResumeVersion.objects.filter(user=request.user, status='complete')
    ctx = {'resumes': resumes, 'need_paste': False, 'url': '', 'pasted': ''}
    if request.method == 'POST':
        rv = resumes.filter(pk=request.POST.get('resume') or 0).first()
        url, pasted = request.POST.get('url', '').strip(), request.POST.get('pasted', '').strip()
        ctx.update(url=url, pasted=pasted)
        title, text = request.POST.get('title', '').strip(), pasted
        if not rv:
            messages.error(request, 'Pick one of your resume versions first.')
        elif not (url or pasted):
            messages.error(request, 'Paste a job link or the job description.')
        else:
            if url and not pasted:
                try:
                    title, text = fetch_job_text(url)
                except FetchError as e:
                    messages.warning(request, f'{e} Please paste the job description text instead.')
                    ctx['need_paste'] = True
                    return render(request, 'job_checker.html', ctx)
            req = extract_skills(text)
            if not req:
                messages.warning(request, 'No known skills were found in that text. Paste the full job description.')
                ctx['need_paste'] = True
                return render(request, 'job_checker.html', ctx)
            have = {s.lower() for s in rv.skills}
            matched = [s for s in req if s in have]
            missing = [s for s in req if s not in have]
            unclear = [f'The job mentions "{m.group(0)}" - confirm your experience.'
                       for m in re.finditer(r'\d+\+?\s*(?:-\s*\d+\s*)?years?', text.lower())][:2]
            job = JobCheck.objects.create(
                user=request.user, resume=rv, url=url, title=title[:200], score=round(100 * len(matched) / len(req)),
                matched=matched, missing=missing, unclear=unclear)
            return redirect('job_result', pk=job.pk)
    return render(request, 'job_checker.html', ctx)


@login_required
def result(request, pk):
    job = get_object_or_404(JobCheck, pk=pk, user=request.user)
    return render(request, 'job_results.html', {'job': job, 'tasks': job.tasks.select_related('topic')})


@login_required
@require_POST
def decide(request, pk):
    job = get_object_or_404(JobCheck, pk=pk, user=request.user)
    if request.POST.get('choice') == 'accept':
        job.tasks.all().delete()
        topics = {t.skill: t for t in Topic.objects.exclude(skill='').order_by('-order')}
        rows = [(topics.get(s), s) for s in job.missing]
        rows.sort(key=lambda r: r[0].order if r[0] else 99)
        PlanTask.objects.bulk_create([PlanTask(job=job, skill=s, topic=t, order=i) for i, (t, s) in enumerate(rows)])
        job.status = 'accepted'
        messages.success(request, 'Plan accepted - tasks added in learning order.')
    else:
        job.tasks.all().delete()
        job.status = 'declined'
        messages.info(request, 'Declined. The analysis is saved in History; no tasks were added.')
    job.save()
    return redirect('job_result', pk=job.pk)


@login_required
@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(PlanTask, pk=pk, job__user=request.user)
    task.done = not task.done
    task.save()
    job = task.job
    done = job.tasks.filter(done=True).count()
    job.status = 'completed' if done == job.tasks.count() else 'in_progress' if done else 'accepted'
    job.save()
    return redirect('job_result', pk=job.pk)


@login_required
@require_POST
def delete(request, pk):
    get_object_or_404(JobCheck, pk=pk, user=request.user).delete()
    messages.success(request, 'Job check and its plan tasks deleted.')
    return redirect('history')
