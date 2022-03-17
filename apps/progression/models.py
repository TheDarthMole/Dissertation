from django.db import models
from apps.learn.models import ExploitType, Lesson, total_lessons_completed
from apps.containers.models import Image, total_images_completed


# Create your models here.
class Progression(models.Model):
    pass


def user_progress_percentage(user, exploit_type):

    image_count, total_images = total_images_completed(user, exploit_type)
    lesson_count, total_lessons = total_lessons_completed(user, exploit_type)

    if total_images + total_lessons == 0:
        return 0

    return round((image_count + lesson_count) / (total_images + total_lessons) * 100, 1)
