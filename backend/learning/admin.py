from django.contrib import admin
from .models import Topic, ExamQuestion, ExamAttempt, StudySession


class QInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'skill')
    inlines = [QInline]


admin.site.register([ExamAttempt, StudySession])
