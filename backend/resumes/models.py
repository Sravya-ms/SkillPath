from django.conf import settings
from django.db import models


class ResumeVersion(models.Model):
    STATUS = [('pending', 'Pending'), ('complete', 'Complete'), ('failed', 'Failed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    # Vercel's disk is read-only, so the uploaded file is kept in the database.
    # It is never served publicly; only the owner's pages can reach it.
    file_data = models.BinaryField(editable=False, default=b'')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    skills = models.JSONField(default=list)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.file_name} ({self.uploaded_at:%d %b %Y})'
