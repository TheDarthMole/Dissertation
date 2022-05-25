# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
from django.urls import path

from apps.learn import views

urlpatterns = [
    # The learn page
    path('learn', views.learn, name='learn'),
    path('lesson/<slug:slug>', views.LessonDetailedView.as_view(), name='lesson_detail'),
    path('complete_lesson/<slug:slug>', views.complete_lesson, name='complete_lesson')
]
