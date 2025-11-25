from django import template
register = template.Library()

@register.filter
def indent(level):
    return "—" * (level * 2)
