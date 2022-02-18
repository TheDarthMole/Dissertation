from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Image(models.Model):
    image_name = models.CharField(max_length=32)
    # The image to pull from
    image = models.CharField(max_length=32)
    # The version of the image, latest is default for docker
    tag = models.CharField(max_length=16, null=True, default='latest')
    # JSON string of the exposed ports, e.g. ["25565:25565", "6000:6000"]. Used for the -p flag
    exposed_ports = models.CharField(max_length=150)
    # Alive duration of the containers in seconds. Default is half an hour
    duration = models.IntegerField(default=1800)
    # The default -it flags
    interactive_flag = models.BooleanField(default=False)
    tty_flag = models.BooleanField(default=False)
    # By default, we want the containers to remove itself on close
    rm_flag = models.BooleanField(default=True)


class Container(models.Model):

    def __str__(self):
        return self.container_image.name

    @property
    def container_owner(self):
        return User.objects.get(pk=self.owner_id)

    @property
    def duration(self):
        return self.container_image.duraton

    @property
    def image_name(self):
        return self.container_image.image_name

    @property
    def image(self):
        return self.container_image.image

    @property
    def rm_flag(self):
        return self.container_image.rm_flag

    @property
    def tty_flag(self):
        return self.container_image.tty_flag

    @property
    def interactive_flag(self):
        return self.container_image.interactive_flag

    @property
    def exposed_ports(self):
        return self.container_image.exposed_ports

    # The person who ran the containers
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # The image that the container uses
    container_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    # The container ID once it has been created, 12 is the size of a normal containers
    container_id = models.CharField(max_length=12, blank=True, null=True)
    # When the container was created
    start_time = models.DateTimeField().auto_now_add


