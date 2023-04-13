from django import template


register = template.Library()


@register.filter
def pretty_float(distance: float):
    return format(round(distance), ",").replace(",", " ")
