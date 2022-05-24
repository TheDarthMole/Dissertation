# -*- encoding: utf-8 -*-
from django.urls import path

from apps.containers import views

urlpatterns = [

    # The containers page
    path('challenges', views.containers, name='challenges'),
    path('challenge/<slug:slug>', views.ContainerDetailedView.as_view(), name='challenge_view'),
    path('challenges/submit', views.submit_challenge, name='challenge_submission'),
    path('challenges/start', views.start, name='challenges_start'),
    path('challenges/stop/<slug:slug>', views.stop, name='challenges_stop')
    # Matches any html file
    # re_path(r'^.*\.*', views.containers, name='containers'),

]
