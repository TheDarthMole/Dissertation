from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from apps.learn.models import Lesson, ExploitType, CompletedLesson
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404


@login_required(login_url="/login/")
def learn(request):
    context = {'segment': 'learn',
               'exploit_types': ExploitType.objects.all()}
    html_template = loader.get_template('learn/lessons.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def complete_lesson(request, slug):
    completed_lesson = get_object_or_404(Lesson, slug=slug)
    CompletedLesson.objects.create(user=request.user, lesson=completed_lesson, completed=True)
    return HttpResponseRedirect(reverse('learn'))


class LessonDetailedView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'learn/lesson.html'
