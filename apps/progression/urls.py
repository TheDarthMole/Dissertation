# -*- encoding: utf-8 -*-
from django.urls import path

from apps.progression import views

urlpatterns = [

    # The containers page
    path('progression', views.progression, name='progression'),

]
