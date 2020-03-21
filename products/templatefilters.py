from django import template

register = template.Library()

@register.filter
def get_list(dictionary,key):
    return dict(dictionary).get(key)
