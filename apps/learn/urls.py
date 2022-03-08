# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.learn import views
from apps.learn.views import LessonListView, LessonDetailedView

urlpatterns = [

    # The containers page
    path('learn', views.learn, name='learn'),
    path('lesson/<slug:slug>', LessonDetailedView.as_view(), name='lesson_detail')

]
