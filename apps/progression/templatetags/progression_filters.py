from django import template
from apps.progression.models import user_progress_percentage
register = template.Library()


@register.filter
def completed_by(obj, user):
    return obj.completed_by(user)


@register.filter
def progress_percentage(user, exploit_type):
    return user_progress_percentage(user, exploit_type)
