import os.path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

import apps.containers.models as containers
from apps.accounts.models import CustomUser


def total_lessons_completed(user, exploit_type):
    lessons = Lesson.objects.filter(exploit_type=exploit_type)
    lesson_count = 0

    for lesson in lessons:
        if lesson.completed_by(user):
            lesson_count += 1

    return lesson_count, len(lessons)


class Difficulty:
    difficulty_not_set = '0'
    very_easy = '1'
    easy = '2'
    normal = '3'
    hard = '4'
    very_hard = '5'

    lookup_table = {difficulty_not_set: 'Difficulty Not Set',
                    very_easy: 'Very Easy',
                    easy: 'Easy',
                    normal: 'Normal',
                    hard: 'Hard',
                    very_hard: 'Very Hard',
                    }

    DIFFICULTY_CHOICES = (
        (difficulty_not_set, lookup_table[difficulty_not_set]),
        (very_easy, lookup_table[very_easy]),
        (easy, lookup_table[easy]),
        (normal, lookup_table[normal]),
        (hard, lookup_table[hard]),
        (very_hard, lookup_table[very_hard]),
    )

    def get_label(self, index):
        return self.lookup_table[index]


class ExploitType(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def lessons(self):
        return Lesson.objects.filter(exploit_type=self)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    exploit_type = models.ForeignKey(ExploitType,
                                     related_name='lesson_exploit_type',
                                     on_delete=models.SET_NULL,
                                     null=True)
    owner = models.ForeignKey(CustomUser,
                              related_name='lesson_created',
                              on_delete=models.SET_NULL,
                              null=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    difficulty = models.CharField(
        max_length=1,
        choices=Difficulty.DIFFICULTY_CHOICES,
        default=Difficulty.difficulty_not_set
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[str(self.slug)])

    @property
    def difficulty_str(self):
        return Difficulty().get_label(self.difficulty)

    @property
    def content(self):
        return Content.objects.filter(lesson=self).order_by('order_number')

    @property
    def get_containers(self):
        return containers.Image.objects.filter(pre_lesson=self)

    def completed_by(self, user):
        result = CompletedLesson.objects.filter(lesson=self, user=user)
        if len(result) == 0:
            return False

        if len(result) > 1:
            raise IndexError

        if result[0].completed:
            return True
        return False

    @classmethod
    def total_lessons(cls):
        return Lesson.objects.count()


class Content(models.Model):
    lesson = models.ForeignKey(Lesson,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model__in': ('text',
                                                       'video',
                                                       'image',
                                                       'file')
                                     },
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order_number = models.IntegerField()

    @property
    def is_text(self):
        if self.content_type.model_class() == Text:
            return True
        return False

    @property
    def is_video(self):
        if self.content_type.model_class() == Video:
            return True
        return False

    @property
    def is_file(self):
        if self.content_type.model_class() == File:
            return True
        return False

    @property
    def is_image(self):
        if self.content_type.model_class() == Image:
            return True
        return False


class ItemBase(models.Model):
    owner = models.ForeignKey(CustomUser,
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
    file_content = models.FileField(upload_to='apps/static/files/lessons')

    @property
    def get_absolute_url(self):
        # Basically return '/static/files/lessons/[file name]'
        # By default the self.file_content returns '/apps/static/files/lessons/...'
        return "/" + "/".join(self.file_content.__str__().split("/")[1:])

    @property
    def file_name(self):
        return self.file_content.__str__().split("/")[-1]

    @property
    def file_size(self):
        return os.path.getsize(self.file_content.__str__())


class Image(ItemBase):
    image_content = models.ImageField(upload_to='apps/static/images/lessons')

    @property
    def get_absolute_url(self):
        # Basically return '/static/images/lessons/[file name]'
        # By default the self.image_contents returns '/apps/static/images/lessons/...'
        return "/" + "/".join(self.image_content.__str__().split("/")[1:])


class Video(ItemBase):
    video_content = models.URLField()

    @property
    def youtube_embed(self):
        url_split = self.video_content.lstrip("https://").lstrip("http://").split("/")
        domain = url_split[0]
        arguments = url_split[1]

        if 'youtube.com' in domain.lower():
            video_id = arguments.split("?v=")[1]
            return f"https://www.youtube.com/embed/{video_id}"

        elif 'youtu.be' in domain.lower():
            return f"https://www.youtube.com/embed/{arguments}"

        raise NotImplemented

    @property
    def get_iframe(self):
        url_split = self.video_content.lstrip("https://").lstrip("http://").split("/")
        domain = url_split[0]
        if domain in ('youtu.be', 'youtube.com'):
            return self.youtube_embed

        # More content types to come?
        raise NotImplemented


class CompletedLesson(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    @classmethod
    def num_completed_lessons(cls, user):
        return CompletedLesson.objects.filter(user=user, completed=True).count()

    @classmethod
    def last_lesson_completed_by(cls, user):
        return CompletedLesson.objects.filter(user=user).last()
