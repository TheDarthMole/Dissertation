from django import template
import datetime
register = template.Library()

def intToTime(value):
    return datetime.timedelta(seconds=value)

register.filter("intToTime", intToTime)
