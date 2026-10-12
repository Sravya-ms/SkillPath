from django.conf import settings
from django.db import models


class JobCheck(models.Model):
    STATUS = [('suggested', 'Suggested'), ('accepted', 'Accepted'), ('in_progress', 'In progress'),
              ('completed', 'Completed'), ('declined', 'Declined')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_checks')
    resume = models.ForeignKey('resumes.ResumeVersion', on_delete=models.SET_NULL, null=True, related_name='job_checks')
    url = models.URLField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=120, blank=True)
    score = models.PositiveSmallIntegerField()
    matched = models.JSONField(default=list)
    missing = models.JSONField(default=list)
    unclear = models.JSONField(default=list)
    status = models.CharField(max_length=12, choices=STATUS, default='suggested')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class PlanTask(models.Model):
    job = models.ForeignKey(JobCheck, on_delete=models.CASCADE, related_name='tasks')
    skill = models.CharField(max_length=40)
    topic = models.ForeignKey('learning.Topic', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    done = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']
