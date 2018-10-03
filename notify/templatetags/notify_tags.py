from django import template
from django.template.loader import render_to_string
from django.conf import settings

register = template.Library()


@register.simple_tag
def display(obj, request=None):
    tpl = getattr(settings, 'NOTIFICATION_TEMPLATES').get(obj.verb)

    if not tpl:
        return ''

    context = {
        'notification': obj,
        'actor': obj.actor,
        'target': obj.target,
        'request': request,
    }
    return render_to_string(tpl, context=context)
