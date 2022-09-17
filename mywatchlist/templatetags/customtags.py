from django import template

register = template.Library()


@register.filter
def count_not_watched(value):
    return sum([not i.watched for i in value])


@register.filter
def count_watched(value):
    return sum([i.watched for i in value])
