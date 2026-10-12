from django.contrib import admin
from .models import ResumeVersion


@admin.register(ResumeVersion)
class ResumeVersionAdmin(admin.ModelAdmin):
    # Metadata only. Admins do not browse students' resume content.
    list_display = ('file_name', 'user', 'uploaded_at', 'status')
    exclude = ('file_data', 'skills')
    readonly_fields = ('user', 'file_name', 'status')
