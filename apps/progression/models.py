from django.db import models
from apps.learn.models import ExploitType, Lesson
from apps.containers.models import Image
import math


# Create your models here.
class Progression(models.Model):
    pass


def user_progress_percentage(user, exploit_type):
    images = Image.objects.filter(exploit_type=exploit_type)
    lessons = Lesson.objects.filter(exploit_type=exploit_type)

    image_count = 0
    lesson_count = 0
    print(images)
    print(lessons)
    for lesson in lessons:
        if lesson.completed_by(user):
            lesson_count += 1

    for image in images:
        if image.completed_by(user):
            image_count += 1
    if len(images) + len(lessons) == 0:
        return 0
    return round((image_count + lesson_count) / (len(images) + len(lessons)) * 100, 1)
