# -*- encoding: utf-8 -*-
"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
from django.urls import path

from apps.progression import views

urlpatterns = [

    # The containers page
    path('progression', views.progression, name='progression'),

]
