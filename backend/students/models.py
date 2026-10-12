from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    education = models.CharField(max_length=120, blank=True)
    career_goal = models.CharField(max_length=120, blank=True)
