# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.learn import views

urlpatterns = [

    # The containers page
    path('learn', views.learn, name='learn'),
    path('lesson', views.lesson, name='lesson')

]
