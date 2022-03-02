from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ExploitType(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    exploit_type = models.ForeignKey(ExploitType,
                                     related_name='lesson_exploit_type',
                                     on_delete=models.SET_NULL,
                                     null=True)
    owner = models.ForeignKey(User,
                              related_name='lesson_created',
                              on_delete=models.SET_NULL,
                              null=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    difficulty_not_set = 0
    very_easy = 1
    easy = 2
    normal = 3
    hard = 4
    very_hard = 5

    DIFFICULTY_CHOICES = (
        (difficulty_not_set, 'Difficulty Not Set'),
        (very_easy, 'Very Easy'),
        (easy, 'Easy'),
        (normal, 'Normal'),
        (hard, 'Hard'),
        (very_hard, 'Very Hard')
    )

    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=difficulty_not_set
    )

    def __str__(self):
        return self.title


class Content(models.Model):
    lesson = models.ForeignKey(Lesson,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model_in': ('text',
                                                      'video',
                                                      'image',
                                                      'file')
                                     },
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
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
