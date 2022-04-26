from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    @property
    def points(self):
        # Importing here is a bit dirty, but it fixes a circular import
        import apps.containers.models as containers
        return containers.points_for(self)

    def __str__(self):
        return self.username
