from django import template

register = template.Library()

@register.filter(name='set_attr')
def set_attr(value, arg):
    attrs = {}
    for attribute in arg.split(','):
        key, val = attribute.split('=')
        attrs[key] = val
    return value.as_widget(attrs=attrs)
