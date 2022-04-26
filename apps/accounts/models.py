from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

    @property
    def points(self):
        # return points_for(self)
        return
    def __str__(self):
        return self.username
