from bleach import clean as bleach_clean
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
from markdownx.utils import markdownify

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return urlencode(query)


@register.filter
def markdown(value):
    return mark_safe(markdownify(bleach_clean(value)))
