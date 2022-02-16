from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Container(models.Model):

    @property
    def container_owner(self):
        return User.objects.get(pk=self.owner_id)

    # The person who ran the containers
    owner_id = models.CharField(max_length=30)
    # Info about the containers
    container_name = models.CharField(max_length=30)
    container_image = models.CharField(max_length=30)
    container_id = models.CharField(max_length=12, blank=True, null=True) # 12 is the size of a normal containers
    # Alive duration of the containers in seconds
    duration = models.IntegerField()
    # JSON string of the exposed ports, e.g. ["25565:25565", "6000:6000"]. Used for the -p flag
    exposed_ports = models.CharField(max_length=150)
    # The default -it flags
    interactive_flag = models.BooleanField(default=False)
    tty_flag = models.BooleanField(default=False)
    # By default, we want the containers to remove itself on close
    rm_flag = models.BooleanField(default=True)
