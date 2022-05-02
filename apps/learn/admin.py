from django.contrib import admin
from .models import ExploitType, Lesson, CompletedLesson


@admin.register(ExploitType)
class ExploitTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'exploit_type', 'owner', 'slug', 'overview', 'created']


@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed']
