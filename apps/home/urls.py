# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""

from django.urls import path, re_path

from apps.home import views

urlpatterns = [

    # The original home page
    path('', views.index, name='home'),

    # The original home page
    path('dashboard', views.index_original, name='home_original'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
