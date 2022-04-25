from django.db import models
from django.contrib.auth.models import User
from apps.learn.models import ExploitType, Lesson
import datetime


def total_images_completed(user, exploit_type):
    images = Image.objects.filter(exploit_type=exploit_type)
    image_count = 0

    for image in images:
        if image.completed_by(user):
            image_count += 1

    return image_count, len(images)


class Image(models.Model):

    def __str__(self):
        return self.image_name

    image_name = models.CharField(max_length=32)
    # The image to pull from
    image = models.CharField(max_length=32)
    # The version of the image, latest is default for docker
    tag = models.CharField(max_length=16, null=True, default='latest')
    # JSON string of the exposed ports, e.g. ["25565:25565", "6000:6000"]. Used for the -p flag
    exposed_ports = models.CharField(max_length=150, default="{}")
    # A JSON string of all environment variables to be used in the containers
    environment = models.CharField(max_length=300, default="{}")
    # Alive duration of the containers in seconds. Default is half an hour
    duration = models.IntegerField(default=1800)
    # The default -it flags
    interactive_flag = models.BooleanField(default=False)
    tty_flag = models.BooleanField(default=False)
    # By default, we want the containers to remove itself on close
    rm_flag = models.BooleanField(default=True)
    # Exploit type of the container
    exploit_type = models.ForeignKey(ExploitType,
                                     related_name='exploit_type',
                                     on_delete=models.CASCADE,
                                     null=True)
    # A lesson that should be completed before the container
    pre_lesson = models.ForeignKey(Lesson,
                                   related_name='lesson',
                                   on_delete=models.CASCADE,
                                   null=True)

    point_reward = models.IntegerField(default=0)

    # the code for the container that the users can edit, this is pulled into the Container instance
    code = models.TextField(null=True, blank=True)
    command = models.TextField(default="mvn test")
    file_location = models.TextField(null=True, blank=True)

    def completed_by(self, user):
        result = CompletedImage.objects.filter(image=self, user=user)
        if len(result) == 0:
            return False

        if len(result) > 1:
            raise IndexError

        if result[0].completed:
            return True
        return False


class Container(models.Model):

    def __str__(self):
        return self.container_image.image_name

    @property
    def container_owner(self):
        return self.owner_id.username

    @property
    def duration(self):  # Show the remaining duration in seconds
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        diff = (now - self.start_time).seconds
        return self.container_image.duration - diff

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
    # The container ID once it has been created, having issues with naming it 'container_id' so it's named slug
    slug = models.SlugField(max_length=16, unique=True, default='0'*16)
    # When the container was created
    start_time = models.DateTimeField(default=datetime.datetime.utcnow, blank=True)
    # The base64 encoded code for the container
    code = models.TextField(null=True, blank=True)


    # Override the save method so that we force the creation of the code field, pulling from Image.code
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.container_image.code

        super(Container, self).save(*args, **kwargs)


class CompletedImage(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    # TODO: Expand this to be dynamic to the content completed in future
    # @property
    # def completed(self) -> bool:
    #     return self.completed
