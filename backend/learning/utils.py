import datetime
from django.utils import timezone
from .models import StudySession


def today_sessions(user):
    today = timezone.localdate()
    return [(s, s.state_on(today)) for s in StudySession.objects.filter(user=user).select_related('topic')
            if s.occurs_on(today)]


def reminders(user):
    """In-app fallback reminders: sessions starting within the next 60 minutes."""
    now = timezone.localtime()
    soon = (now + datetime.timedelta(minutes=60)).time()
    return [s for s, st in today_sessions(user)
            if s.remind and st == 'planned' and now.time() <= s.start <= soon]
