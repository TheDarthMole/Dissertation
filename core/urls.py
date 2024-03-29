# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("apps.containers.urls")),  # The containers files
    path("", include("apps.learn.urls")),  # The course content files
    path("", include("apps.progression.urls")),  # The progression of the user
    path("", include("apps.scoreboard.urls")),  # The scoreboards of users
    path("", include("apps.home.urls")),  # UI Kits Html files
]
