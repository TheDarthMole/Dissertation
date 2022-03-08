from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson, ExploitType
from django.views.generic import ListView, DetailView


# Create your views here.

@login_required(login_url="/login/")
def progression(request):
    context = {'segment': 'progression'}
    html_template = loader.get_template('progression/progression.html')
    return HttpResponse(html_template.render(context, request))
