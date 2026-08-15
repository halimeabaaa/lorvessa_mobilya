from django import template
from pages.image_utils import best_full_url, best_thumb_url

register = template.Library()


@register.filter
def thumb_url(file_field):
    """Galeri kartı için optimize thumbnail URL."""
    try:
        return best_thumb_url(file_field)
    except Exception:
        return getattr(file_field, 'url', '') or ''


@register.filter
def full_url(file_field):
    """Lightbox / hero için optimize full URL."""
    try:
        return best_full_url(file_field)
    except Exception:
        return getattr(file_field, 'url', '') or ''
