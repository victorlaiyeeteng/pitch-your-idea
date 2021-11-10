from django import template
from ..models import *

register=template.Library()

@register.simple_tag

@register.filter
def order_by(queryset, args):
    args = [x for x in args]
    return queryset.order_by(*args)

@register.filter
def in_chat(notifications, chat): 
    return notifications.filter(chat=chat)