from django import template

from apps.progression.models import Progression

register = template.Library()


@register.filter
def completed_by(obj, user):
    return obj.completed_by(user)


@register.filter
def progress_percentage(user, exploit_type):
    return Progression.user_progress_percentage(user, exploit_type)
