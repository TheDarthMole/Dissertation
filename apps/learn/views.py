from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson, ExploitType
from django.views.generic import ListView, DetailView


# Create your views here.


@login_required(login_url="/login/")
def learn(request):
    context = {'exploit_types': ExploitType.objects.all()}
    for x in ExploitType.objects.all():
        print(x)
    html_template = loader.get_template('learn/lessons.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def lesson(request):
    context = {}  # {'lesson': Lesson}
    html_template = loader.get_template('learn/lesson.html')
    return HttpResponse(html_template.render(context, request))


class LessonListView(ListView):
    model = Lesson
    template_name = 'learn/lessons.html'


class LessonDetailedView(DetailView):
    model = Lesson
    template_name = 'learn/lesson.html'
