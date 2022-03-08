# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.containers import views

urlpatterns = [

    # The containers page
    path('challenges', views.container, name='challenges'),
    path('challenges/start', views.start, name='challenges_start'),  # , name='start_container'
    path('challenges/stop', views.stop, name='challenges_stop')
    # Matches any html file
    # re_path(r'^.*\.*', views.containers, name='containers'),

]
