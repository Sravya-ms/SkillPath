from django.contrib import admin
from .models import CareerPath, CareerSkill


class SkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1


@admin.register(CareerPath)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SkillInline]
