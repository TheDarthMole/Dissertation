# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
from django.urls import path

from apps.scoreboard import views

urlpatterns = [

    # The scoreboard page
    path('scoreboard', views.scoreboard, name='scoreboard'),

]
