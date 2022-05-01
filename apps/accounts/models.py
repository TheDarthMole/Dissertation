from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    @property
    def points(self):
        # Importing here is a bit dirty, but it fixes a circular import
        import apps.containers.models as containers
        return containers.points_for(self)

    @property
    def last_completed_lesson(self):
        from apps.learn.models import CompletedLesson
        last = CompletedLesson.last_lesson_completed_by(self)
        if last:
            return last.lesson.title
        return "N/A"

    @property
    def last_completed_challenge(self):
        from apps.containers.models import CompletedImage
        last = CompletedImage.last_challenge_completed_by(self)
        if last:
            return last.image.image_name
        return "N/A"

    def __str__(self):
        return self.username
