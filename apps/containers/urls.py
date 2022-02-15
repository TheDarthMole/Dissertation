# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.containers import views

urlpatterns = [

    # The containers page
    path('containers', views.container, name='containers'),

    # Matches any html file
    # re_path(r'^.*\.*', views.container, name='containers'),

]
