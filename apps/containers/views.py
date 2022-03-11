import docker
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from apps.containers.models import Container, Image


@login_required(login_url="/login/")
def container(request):
    context = {'segment': 'containers',
               'containers': Container.objects.all(),
               'images': Image.objects.all()}
    html_template = loader.get_template('containers/containers.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def start(request):
    if request.method == 'POST':

        client = docker.from_env()
        try:
            image_id = int(request.POST.get('imageID', ''))
            image_obj = Image.objects.filter(id=image_id)

            if len(image_obj) != 1:
                raise ValueError

            image_obj = image_obj[0]

            new_container = Container(owner_id=request.user,
                                      container_image=image_obj)
            # Parse JSON strings
            port_mappings = json.loads(image_obj.exposed_ports)
            environment = json.loads(image_obj.environment)

            kwargs = {'detach': True,
                      'auto_remove': image_obj.rm_flag,
                      'tty': image_obj.tty_flag,
                      'stdin_open': image_obj.interactive_flag,
                      'ports': port_mappings,
                      'environment': environment
                      }
            if not image_obj.rm_flag:  # Mutually exclusive events
                kwargs['restart_policy'] = {"Name": "always"}

            client.containers.run(image_obj.image, **kwargs)

            new_container.save()

        except ValueError:
            print("Oopa, something happened!")

    return redirect(reverse("challenges"))


@login_required(login_url="/login/")
def stop(request, container_id):
    print(container_id)
    valid_container = Container.objects.filter(id=container_id, owner_id=request.user)

    if len(valid_container) != 1:
        messages.error(request, "Error, that container does not exist")
        return redirect(reverse("challenges"))

    client = docker.from_env()

    try:
        image_id = int(request.POST.get('imageID', ''))
        image_obj = Image.objects.filter(id=image_id)

    except:
        pass

    messages.info(request, "Error, that container does not exist")
    return redirect(reverse("challenges"))