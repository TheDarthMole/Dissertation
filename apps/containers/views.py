from time import sleep
import docker
import json
import random
import string
import base64

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView

from apps.containers.models import Container, Image, CompletedImage


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@login_required(login_url="/login/")
def containers(request):
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
                                      container_image=image_obj,
                                      slug=randomword(16))

            new_container.save()

        except ValueError as e:
            print(f"Oopa, something happened! {e}")

    return redirect('challenge_view', slug=new_container.slug)


def remove_broken_containers():
    containers_web_app = Container.objects.all()
    client = docker.from_env()

    for container_app in containers_web_app:
        try:
            client.containers.get(container_app.slug)
        except docker.errors.NotFound:
            container_app.delete()

    # Search for mismatched containers that are started in docker but don't have a record
    containers_docker = client.containers.list(all=True)
    for container_docker in containers_docker:
        # If the container is made for the app (Don't inspect apps not started by the app)
        if container_docker.name[:5] == "cntr_" and len(container_docker.name) == 15:
            # Search for the container in the app database
            filtered_container = Container.objects.filter(slug=container_docker.id)
            if len(filtered_container) != 1:
                try:
                    container_docker.remove(force=True, v=True)
                except docker.errors.APIError:
                    print(f"There was an error stopping & removing the container: {container_docker.id}")


@login_required(login_url="/login/")
def stop(request, slug):
    valid_container = Container.objects.filter(slug=slug, owner_id=request.user)

    if len(valid_container) != 1:
        messages.error(request, "Error, that container does not exist")
        return redirect(reverse("challenges"))

    client = docker.from_env()
    try:
        # Get the container to stop
        try:
            docker_container = client.containers.get(valid_container[0].slug)
        except docker.errors.NotFound:
            print(f"Container {valid_container[0].slug} not found!")
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
        print(f"There was an error stopping & removing the container: {docker_container.id}")

    return redirect(reverse("challenges"))


class ContainerDetailedView(LoginRequiredMixin, DetailView):
    model = Container
    segment = {}

    template_name = 'containers/container.html'

    # override context data so that we can set segment as containers
    def get_context_data(self, *args, **kwargs):
        context = super(ContainerDetailedView,
                        self).get_context_data(*args, **kwargs)
        # add extra field
        context["segment"] = "containers"
        return context


@login_required(login_url="/login/")
def submit_challenge(request):
    if request.method == 'POST':
        b64code = request.POST.get('form_b64_code')
        code = base64.b64decode(b64code).decode('utf8')
        container_id = request.POST.get('form_container')

        container = Container.objects.filter(slug=container_id)[0]

        # container = Container.objects.filter(container_id)[0]

        docker_client = docker.from_env()
        image_obj = container.container_image

        container.code = code
        container.save()

        port_mappings = json.loads(image_obj.exposed_ports)
        environment = json.loads(image_obj.environment)

        # Overwrite the file in the container with the user's file, then compile it using the image's command
        # Docker 'fails' if using 'mvn test', as it returns a non-zero value, using '|| true' makes sure
        # it is always a zero return
        command = f"bash -c \"echo -n '{b64code}' | base64 -d > {image_obj.file_location}; {image_obj.command} " \
                  f"|| true \" "

        kwargs = {'detach': False,
                  'auto_remove': True,  # image_obj.rm_flag
                  'tty': image_obj.tty_flag,
                  'stdin_open': image_obj.interactive_flag,
                  'ports': port_mappings,
                  'environment': environment,
                  'name': f'cntr_{randomword(10)}',
                  # The code directory is expected to be in /source, eg. /source/pom.xml
                  'working_dir': '/source',
                  'command': command
                  }

        try:
            docker_container = docker_client.containers.run(image_obj.image, **kwargs)
        except Exception as e:
            print(f"An error occurred! {e}")

        logs = str(docker_container, 'utf8')

        if "COMPILATION ERROR" in logs:
            messages.add_message(request, messages.ERROR,
                                 f"Your code failed to compile!")
            # @TODO make the error message more useful!
            return redirect('challenge_view', slug=container.slug)

        # print("logs: " + logs)

        start_index = logs.rfind("Tests run:")
        end_index = logs.find("\n", start_index)
        results = logs[start_index:end_index]
        split = results.split(": ")

        runs = int(split[1].split(",")[0])
        failures = int(split[2].split(",")[0])
        skipped = int(split[3].split(",")[0])

        # print(f"Runs: {runs}, Failures: {failures}, Skipped: {skipped}")

        if failures == 0:
            # Success! They fixed the issue
            messages.add_message(request, messages.SUCCESS, f"Well done! You completed {container.container_image}!")

            container.delete()
            # If the user has completed previously, the update it, else add the new completed image
            CompletedImage.objects.update_or_create(user=request.user, image=image_obj, completed=True)
            return redirect('challenges')
        else:
            # There were errors!
            messages.add_message(request, messages.ERROR,
                                 f"Your code did not pass the inspection. There are {failures} JUnit failures for " +
                                 f"{container.container_image}!")

            return redirect('challenge_view', slug=container.slug)

        # return
