from pathlib import PurePosixPath

from django import template

register = template.Library()


@register.filter
def thumb_url(file_field):
    """Git ile yayınlanan statik galeri küçük görselinin adresi."""
    rel = _relative_name(file_field)
    if not rel:
        return ''
    path = PurePosixPath(rel)
    return f'/static/media/{path.parent}/{path.stem}_thumb.webp'


@register.filter
def full_url(file_field):
    """Git ile yayınlanan statik WebP görselinin adresi."""
    rel = _relative_name(file_field)
    if not rel:
        return ''
    return f'/static/media/{PurePosixPath(rel).with_suffix(".webp")}'


def _relative_name(file_field):
    name = getattr(file_field, 'name', '') or str(file_field or '')
    name = name.replace('\\', '/').lstrip('/')
    for prefix in ('static/media/', 'media/'):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name
