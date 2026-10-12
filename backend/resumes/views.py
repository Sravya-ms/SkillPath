from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from careers.skills import extract_skills
from .models import ResumeVersion

MAX_BYTES = 5 * 1024 * 1024


def check_file(f):
    name = f.name.lower()
    if f.size > MAX_BYTES:
        return 'That file is larger than 5 MB.'
    head = f.read(4)
    f.seek(0)
    if (name.endswith('.pdf') and head == b'%PDF') or (name.endswith('.docx') and head[:2] == b'PK'):
        return None
    return 'Please upload a genuine PDF or DOCX file.'


def extract_text(f, name):
    if name.lower().endswith('.pdf'):
        import pdfplumber
        with pdfplumber.open(f) as pdf:
            return '\n'.join((p.extract_text() or '') for p in pdf.pages)
    import docx
    return '\n'.join(p.text for p in docx.Document(f).paragraphs)


@login_required
def upload(request):
    if request.method == 'POST':
        f = request.FILES.get('resume')
        err = check_file(f) if f else 'Choose a file first.'
        if err:
            messages.error(request, err)
            return redirect('upload')
        rv = ResumeVersion(user=request.user, file_name=f.name[:255])
        try:
            skills = extract_skills(extract_text(f, f.name))
            f.seek(0)
            rv.status, rv.skills = 'complete', skills
        except Exception:
            rv.status = 'failed'
        rv.file = f
        rv.save()
        if rv.status == 'failed':
            messages.error(request, 'We could not read that file. Try another copy, or add your skills by hand.')
        return redirect('review', pk=rv.pk)
    return render(request, 'resume_upload.html')


@login_required
def review(request, pk):
    rv = get_object_or_404(ResumeVersion, pk=pk, user=request.user)
    if request.method == 'POST':
        raw = request.POST.get('skills', '')
        rv.skills = sorted({s.strip().lower()[:40] for s in raw.split(',') if s.strip()})
        rv.status = 'complete'
        rv.save()
        return redirect('results', pk=rv.pk)
    return render(request, 'resume_review.html', {'rv': rv, 'skills_csv': ','.join(rv.skills)})


@login_required
@require_POST
def delete(request, pk):
    rv = get_object_or_404(ResumeVersion, pk=pk, user=request.user)
    rv.file.delete(save=False)
    rv.delete()
    messages.success(request, 'Resume version deleted.')
    return redirect('history')
