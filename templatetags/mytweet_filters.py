from django import template
register = template.Library()


@register.filter
def capitalize(value):
    return value.capitalize()