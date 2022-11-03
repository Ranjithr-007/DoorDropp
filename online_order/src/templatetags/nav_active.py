from django import template
from django.urls import reverse, resolve, Resolver404

register = template.Library()


@register.simple_tag
def active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return "active"

    return ""
