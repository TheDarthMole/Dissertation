from django.shortcuts import render

# Create your views here.

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

@login_required(login_url="/login/")
def container(request):
    context = {'segment': 'containers'}
    print("Triggered!!!")
    html_template = loader.get_template('containers/container.html')
    return HttpResponse(html_template.render(context, request))
