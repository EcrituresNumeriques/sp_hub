from datetime import datetime
from django import template

register = template.Library()

@register.filter("parse_timestamp")
def parse_timestamp(value):
    value = float(value)
    try:
        return datetime.fromtimestamp(value)
    except AttributeError:
        return ''
