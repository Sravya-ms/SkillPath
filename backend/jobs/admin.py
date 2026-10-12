from django.contrib import admin
from .models import JobCheck, PlanTask
admin.site.register([JobCheck, PlanTask])
