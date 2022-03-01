from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ExploitType(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    exploit_type = models.ForeignKey(ExploitType, related_name='lesson_exploit_type')
    owner = models.ForeignKey(User, related_name='lesson_created')
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    DIFFICULTY_CHOICES = (
        (0, 'Difficulty'),
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Normal'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    )
    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=0
    )

    def __str__(self):
        return self.title


class Content(models.Model):
    pass


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    text_content = models.TextField()


class File(ItemBase):
    file_content = models.FileField(upload_to='files')


class Image(ItemBase):
    image_content = models.FileField(upload_to='images')


class Video(ItemBase):
    video_content = models.URLField()
