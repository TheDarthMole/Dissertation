# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from apps.containers import views

urlpatterns = [

    # The containers page
    path('challenges', views.container, name='challenges'),
    path('challenges/start', views.start, name='challenges_start'),  # , name='start_container'
    path('challenges/stop/<int:container_id>', views.stop, name='challenges_stop')
    # Matches any html file
    # re_path(r'^.*\.*', views.containers, name='containers'),

]
