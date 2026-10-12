from urllib.parse import quote_plus
from django.conf import settings
from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=80, unique=True)
    skill = models.CharField(max_length=40, blank=True, help_text='Canonical skill this topic teaches')
    order = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)
    careers = models.ManyToManyField('careers.CareerPath', related_name='topics', blank=True)

    class Meta:
        ordering = ['order', 'title']

    @property
    def youtube_url(self):
        # Honest fallback: a search link, never an invented video URL. Admins can curate later.
        return 'https://www.youtube.com/results?search_query=' + quote_plus(f'{self.title} tutorial for beginners')

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=300)
    options = models.JSONField(help_text='List of 4 answer strings')
    correct = models.PositiveSmallIntegerField(help_text='Index (0-3) of the correct option')

    def __str__(self):
        return self.text[:60]


class ExamAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    passed = models.BooleanField()
    attempt_no = models.PositiveSmallIntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-taken_at']


class StudySession(models.Model):
    REPEAT = [('none', 'Once'), ('daily', 'Every day'), ('weekdays', 'Weekdays'), ('weekly', 'Weekly')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    repeat = models.CharField(max_length=10, choices=REPEAT, default='none')
    remind = models.BooleanField(default=True)
    paused = models.BooleanField(default=False)
    last_done = models.DateField(null=True, blank=True)
    last_missed = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['start']

    def occurs_on(self, d):
        if self.paused or d < self.date:
            return False
        return {'none': d == self.date, 'daily': True, 'weekdays': d.weekday() < 5,
                'weekly': d.weekday() == self.date.weekday()}[self.repeat]

    def state_on(self, d):
        return 'done' if self.last_done == d else 'missed' if self.last_missed == d else 'planned'
