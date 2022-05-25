"""
 * Copyright (C) Nicholas Ruffles - All rights reserved
 * Written by Nicholas Ruffles (Nicholas.Ruffles@protonmail.com)
"""
from django.apps import AppConfig


class ScoreboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.scoreboard'
