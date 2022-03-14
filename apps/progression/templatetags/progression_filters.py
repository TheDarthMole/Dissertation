from django import template

register = template.Library()


@register.filter
def completed_by(obj, user):
    return obj.completed_by(user)
