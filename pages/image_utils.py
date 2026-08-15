"""Medya optimizasyonu: WebP + thumbnail üretimi."""
from __future__ import annotations

import io
from pathlib import Path

from django.conf import settings
from PIL import Image, ImageOps

FULL_MAX = 1600
THUMB_MAX = 720
WEBP_QUALITY = 78
THUMB_QUALITY = 72


def _media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def relative_media_path(file_field) -> str | None:
    if not file_field:
        return None
    name = getattr(file_field, 'name', None) or str(file_field)
    return name.replace('\\', '/')


def sibling_path(rel_path: str, suffix: str) -> str:
    p = Path(rel_path)
    return str(p.with_name(f'{p.stem}{suffix}{p.suffix}')).replace('\\', '/')


def webp_rel(rel_path: str) -> str:
    p = Path(rel_path)
    return str(p.with_suffix('.webp')).replace('\\', '/')


def thumb_rel(rel_path: str) -> str:
    p = Path(rel_path)
    return str(p.with_name(f'{p.stem}_thumb.webp')).replace('\\', '/')


def media_url(rel_path: str) -> str:
    base = settings.MEDIA_URL
    if not base.endswith('/'):
        base += '/'
    return base + rel_path.lstrip('/')


def absolute_media_file(rel_path: str) -> Path:
    return _media_root() / rel_path


def exists_media(rel_path: str) -> bool:
    return absolute_media_file(rel_path).is_file()


def optimize_file(source: Path, dest: Path, max_side: int, quality: int) -> bool:
    """Kaynağı WebP olarak kaydeder. Başarılıysa True."""
    try:
        with Image.open(source) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode in ('RGBA', 'P'):
                im = im.convert('RGBA')
            else:
                im = im.convert('RGB')
            im.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
            dest.parent.mkdir(parents=True, exist_ok=True)
            save_kwargs = {'format': 'WEBP', 'quality': quality, 'method': 4}
            if im.mode == 'RGBA':
                im.save(dest, **save_kwargs)
            else:
                im.save(dest, **save_kwargs)
        return True
    except Exception:
        return False


def ensure_optimized(rel_path: str, force: bool = False) -> dict:
    """Orijinal için .webp ve _thumb.webp üretir."""
    result = {'full': None, 'thumb': None, 'created': []}
    if not rel_path:
        return result

    src = absolute_media_file(rel_path)
    if not src.is_file():
        return result

    full = webp_rel(rel_path)
    thumb = thumb_rel(rel_path)
    full_path = absolute_media_file(full)
    thumb_path = absolute_media_file(thumb)

    if force or not full_path.is_file():
        if optimize_file(src, full_path, FULL_MAX, WEBP_QUALITY):
            result['created'].append(full)
    if force or not thumb_path.is_file():
        if optimize_file(src, thumb_path, THUMB_MAX, THUMB_QUALITY):
            result['created'].append(thumb)

    if full_path.is_file():
        result['full'] = full
    if thumb_path.is_file():
        result['thumb'] = thumb
    return result


def best_full_url(file_field) -> str:
    rel = relative_media_path(file_field)
    if not rel:
        return ''
    webp = webp_rel(rel)
    if exists_media(webp):
        return media_url(webp)
    return file_field.url


def best_thumb_url(file_field) -> str:
    rel = relative_media_path(file_field)
    if not rel:
        return ''
    thumb = thumb_rel(rel)
    if exists_media(thumb):
        return media_url(thumb)
    webp = webp_rel(rel)
    if exists_media(webp):
        return media_url(webp)
    return file_field.url
