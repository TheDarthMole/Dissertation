# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.containers import views

urlpatterns = [

    # The containers page
    path('containers', views.container, name='containers'),
    path('containers/start', views.start),  # , name='start_container'
    path('containers/stop', views.stop)
    # Matches any html file
    # re_path(r'^.*\.*', views.containers, name='containers'),

]
