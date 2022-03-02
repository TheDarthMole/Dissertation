from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson


# Create your views here.


@login_required(login_url="/login/")
def learn(request):
    context = {}
    html_template = loader.get_template('learn/lessons.html')
    return HttpResponse(html_template.render(context, request))


def lesson(request):
    context = {}  # {'lesson': Lesson}
    html_template = loader.get_template('learn/lesson.html')
    return HttpResponse(html_template.render(context, request))
