from django import template
from django.utils.html import strip_tags
from html import unescape

register = template.Library()

@register.filter
def clean_content(value):
    # Strip tags, unescape entities (– → -), truncate
    return strip_tags(unescape(value))[:220]