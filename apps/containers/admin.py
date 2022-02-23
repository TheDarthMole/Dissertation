from django.contrib import admin

# Register your models here.
from .models import Container, Image

# admin.site.register(Container)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_owner', 'image_name', 'container_image', 'duration', 'exposed_ports','interactive_flag', 'tty_flag', 'rm_flag']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'image', 'tag', 'exposed_ports', 'environment', 'duration', 'interactive_flag', 'tty_flag', 'rm_flag']
