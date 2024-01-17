from django import template

register = template.Library()

@register.filter(name="split")
def split(value, arg):
    """Extracts country or capital from the label"""
    if arg == 'first':
        return value.split(",")[0]
    if arg == 'second':
        return value.split(",")[1]
    return value
