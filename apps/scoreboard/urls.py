# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from apps.scoreboard import views

urlpatterns = [

    # The scoreboard page
    path('scoreboard', views.scoreboard, name='scoreboard'),

]
