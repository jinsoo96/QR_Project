from django import template
from urllib.parse import unquote

register = template.Library()

@register.filter
def urldecode(value):
    return unquote(value)