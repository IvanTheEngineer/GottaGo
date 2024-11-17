from django import template
from users.models import TravelPlan, FileMetadata, Invite

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
def num_invites(user):
    count = len(Invite.objects.filter(requested_to=user))
    if count == 0:
        return ""
    else:
        return "(" +  str(count) + ")"

@register.filter
def display_role(user):
    if has_group(user, "PMA"):
        return "PMA"
    return "Regular"
