from django import template
import datetime, base64

register = template.Library()


def intToTime(value):
    return datetime.timedelta(seconds=value)


def toBase64(value):
    return base64.b64encode(value.encode("utf8")).decode("utf8")


register.filter("intToTime", intToTime)
register.filter("toBase64", toBase64)
