from django.contrib import admin
from .models import ExploitType, Content, ItemBase, Text, File, Image, Video, Lesson


# Register your models here.
@admin.register(ExploitType)
class ExploitTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'exploit_type', 'owner', 'slug', 'overview', 'created']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'lesson', 'content_type', 'item']


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['text_content']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['file_content']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['video_content']
