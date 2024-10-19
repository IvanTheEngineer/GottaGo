from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def display_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username

@register.filter
def display_role(user):
    if has_group(user, "PMA"):
        return "PMA"
    return "Regular"
