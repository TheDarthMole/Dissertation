# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.learn import views

urlpatterns = [
    # The learn page
    path('learn', views.learn, name='learn'),
    path('lesson/<slug:slug>', views.LessonDetailedView.as_view(), name='lesson_detail'),
    path('complete_lesson/<slug:slug>', views.complete_lesson, name='complete_lesson')
]
