from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson, ExploitType
from apps.progression.models import Progression
from django.views.generic import ListView, DetailView


# Create your views here.

def chunk_results(list, n):
    return [list[i:i+n] for i in range(0, len(list), n)]


@login_required(login_url="/login/")
def progression(request):
    print(list(chunk_results(ExploitType.objects.all(), 3)))
    context = {'segment': 'progression',
               'chunked_exploit_types': list(chunk_results(ExploitType.objects.all(), 3)),
               'progress_obj': Progression(request.user)}
    html_template = loader.get_template('progression/progression.html')
    return HttpResponse(html_template.render(context, request))
