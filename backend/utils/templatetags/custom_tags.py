from django import template

register = template.Library()

@register.filter
def var_to_title(value):
    result = value.replace("_", " ").title()
    return result
