from django.contrib import admin

# Register your models here.
from .models import Container

# admin.site.register(Container)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ['container_owner', 'container_name', 'container_image', 'duration', 'exposed_ports', 'interactive_flag', 'tty_flag', 'rm_flag']