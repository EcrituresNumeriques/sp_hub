from datetime import datetime
from django import template

register = template.Library()

@register.filter("parse_timestamp")
def parse_timestamp(value):
    try:
        return datetime.fromtimestamp(float(value))
    except:
        return value
