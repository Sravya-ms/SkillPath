from .models import CareerPath


def score_resume(skills, limit=5):
    """
    Documented formula (same for every career):
        score = 100 * (sum of weights of required skills found in resume) / (sum of all required weights)
    Results are ESTIMATES, sorted high -> low, top `limit` returned.
    """
    have = {s.lower() for s in skills}
    out = []
    for c in CareerPath.objects.filter(active=True).prefetch_related('skills'):
        rows = list(c.skills.all())
        total = sum(r.weight for r in rows)
        if not total:
            continue
        matched = [r for r in rows if r.skill in have]
        missing = sorted((r for r in rows if r.skill not in have), key=lambda r: -r.weight)
        score = round(100 * sum(r.weight for r in matched) / total)
        reason = (f"You show {len(matched)} of {len(rows)} required skills"
                  + (f" ({', '.join(r.skill for r in matched)})." if matched else '.')
                  + (f" Biggest gaps: {', '.join(r.skill for r in missing[:3])}." if missing else ' No gaps found.'))
        out.append({'career': c, 'score': score, 'matched': [r.skill for r in matched],
                    'missing': [r.skill for r in missing], 'reason': reason})
    out.sort(key=lambda r: (-r['score'], -len(r['matched']), r['career'].title))
    return out[:limit]
