from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson, ExploitType
from django.views.generic import ListView, DetailView


@login_required(login_url="/login/")
def learn(request):
    context = {'segment': 'learn',
               'exploit_types': ExploitType.objects.all()}
    html_template = loader.get_template('learn/lessons.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def lesson(request):
    context = {}  # {'lesson': Lesson}
    html_template = loader.get_template('learn/lesson.html')
    return HttpResponse(html_template.render(context, request))


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'learn/lessons.html'


class LessonDetailedView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'learn/lesson.html'
