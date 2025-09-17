from django import template

register = template.Library()


@register.simple_tag
def get_user_driver_pk(user):
    """Safely get user's driver pk."""
    try:
        if hasattr(user, "driver") and user.driver:
            return user.driver.pk
    except AttributeError:

        return None
    return None


@register.simple_tag
def user_is_driver(user):
    """Check if user is a driver."""
    try:
        return hasattr(user, "driver") and user.driver is not None
    except AttributeError:
        return False
