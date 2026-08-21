from django import template

from pages.image_utils import best_full_url, best_thumb_url

register = template.Library()


@register.filter
def thumb_url(file_field):
    """Yerel optimize görseli, yoksa kalıcı depodaki görseli döndürür."""
    return best_thumb_url(file_field)


@register.filter
def full_url(file_field):
    """Yerel optimize görseli, yoksa kalıcı depodaki görseli döndürür."""
    return best_full_url(file_field)
