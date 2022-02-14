from django.db import models

# Create your models here.

class Containers(models.Model):
    # The person who ran the container
    owner_id = models.CharField(max_length=30)
    # Info about the container
    container_name = models.CharField(max_length=30)
    container_image = models.CharField(max_length=30)
    container_id = models.CharField(max_length=12) # 12 is the size of a normal container
    # Alive duration of the container in seconds
    duration = models.IntegerField()
    # JSON string of the exposed ports, e.g. ["25565:25565", "6000:6000"]. Used for the -p flag
    exposed_ports = models.CharField(max_length=150)
    # The default -it flags
    interactive_flag = models.BooleanField(defaut=False)
    tty_flag = models.BooleanField(defaut=False)
    # By default, we want the container to remove itself on close
    rm_flag = models.BooleanField(defaut=True)
