"""
Template tags
"""
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check group
    """
    return user.groups.filter(name=group_name).exists()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Get latest vaccination of same vaccin
    """
    current_vaccin = None
    for vaccin in dictionary.get(key):
        if current_vaccin is None:
            current_vaccin = vaccin
            continue
        if vaccin.dose_nr > current_vaccin.dose_nr:
            current_vaccin = vaccin
    return [current_vaccin]
