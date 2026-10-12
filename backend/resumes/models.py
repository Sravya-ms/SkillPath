import os, uuid
from django.conf import settings
from django.db import models


def resume_path(instance, filename):
    return f'resumes/{instance.user_id}/{uuid.uuid4().hex}{os.path.splitext(filename)[1].lower()}'


class ResumeVersion(models.Model):
    STATUS = [('pending', 'Pending'), ('complete', 'Complete'), ('failed', 'Failed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to=resume_path)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    skills = models.JSONField(default=list)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.file_name} ({self.uploaded_at:%d %b %Y})'
