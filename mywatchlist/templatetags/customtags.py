from django import template

register = template.Library()


@register.filter
def count_not_watched(value):
    return sum([not i.watched for i in value])


@register.filter
def count_watched(value):
    return sum([i.watched for i in value])


@register.filter
def rating_star(value):
    return int(value) * "⭐"


@register.filter
def modulo(num, val):
    return num % val
