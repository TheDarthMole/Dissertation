import json

import docker
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from apps.containers.models import Container, Image
import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@login_required(login_url="/login/")
def container(request):
    context = {'segment': 'containers',
               'containers': Container.objects.filter(owner_id=request.user),
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
                      'environment': environment,
                      'name': f'cntr_{randomword(10)}'
                      }
            if not image_obj.rm_flag:  # Mutually exclusive events
                kwargs['restart_policy'] = {"Name": "always"}

            container_id = client.containers.run(image_obj.image, **kwargs)
            new_container.container_id = container_id.id

            new_container.save()

        except ValueError:
            print("Oopa, something happened!")

    return redirect(reverse("challenges"))


def remove_broken_containers():
    containers_web_app = Container.objects.all()
    client = docker.from_env()

    for container_app in containers_web_app:
        try:
            client.containers.get(container_app.container_id)
        except docker.errors.NotFound:
            container_app.delete()

    # Search for mismatched containers that are started in docker but don't have a record
    containers_docker = client.containers.list(all=True)
    for container_docker in containers_docker:
        # If the container is made for the app (Don't inspect apps not started by the app)
        if container_docker.name[:5] == "cntr_" and len(container_docker.name) == 15:
            # Search for the container in the app database
            filtered_container = Container.objects.filter(container_id=container_docker.id)
            if len(filtered_container) != 1:
                try:
                    container_docker.remove(force=True, v=True)
                except docker.errors.APIError:
                    print("There was an error stopping & removing the container: " + container_docker.id)

@login_required(login_url="/login/")
def stop(request, container_id):
    valid_container = Container.objects.filter(id=container_id, owner_id=request.user)

    if len(valid_container) != 1:
        messages.error(request, "Error, that container does not exist")
        return redirect(reverse("challenges"))

    client = docker.from_env()
    try:
        # Get the container to stop
        try:
            docker_container = client.containers.get(valid_container[0].container_id)
        except docker.errors.NotFound:
            print(f"Container {valid_container[0].container_id} not found!")
            # The docker container doesn't exist, so the entry is void
            valid_container.delete()

            # May as well check to see if there are other containers that don't exist
            remove_broken_containers()
            return redirect(reverse("challenges"))

        # Stop & remove the container, including associated volumes
        docker_container.remove(force=True, v=True)
        # Remove the entry for the container
        valid_container.delete()

    except docker.errors.APIError:
        print("There was an error stopping & removing the container: " + docker_container.id)

    return redirect(reverse("challenges"))
