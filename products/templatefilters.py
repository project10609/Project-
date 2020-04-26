from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def get_list(dictionary,key):
    return dict(dictionary).get(key)


@register.simple_tag(takes_context=True)
def url_replace(context, next_page):
    query = context['request'].GET.copy().urlencode()

    if '&page=' in query:
        url = query.rpartition('&page=')[0] # equivalent to .split('page='), except more efficient
    else:
        url = query
    return f'{url}&page={next_page}'


@register.filter
def hash(h, key):
    return h[key]
