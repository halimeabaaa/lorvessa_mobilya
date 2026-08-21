from pathlib import Path

from django.conf import settings
from django.db import migrations


IMAGE_SUFFIXES = {'.webp', '.png', '.jpg', '.jpeg'}


def _title(path):
    return ' '.join(part.capitalize() for part in path.stem.replace('_', ' ').split())


def seed_static_catalog_once(apps, schema_editor):
    """Git'teki görselleri sadece bu migration ilk kez uygulanırken kaydet."""
    GalleryItem = apps.get_model('pages', 'GalleryItem')
    SliderImage = apps.get_model('pages', 'SliderImage')
    root = Path(settings.BASE_DIR) / 'static' / 'media'

    for folder_name, model in (
        ('gallery', GalleryItem),
        ('slider', SliderImage),
    ):
        folder = root / folder_name
        if not folder.is_dir():
            continue

        existing = set(model.objects.values_list('image', flat=True))
        order = model.objects.count()
        for path in sorted(folder.iterdir(), key=lambda item: item.name.casefold()):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            if path.stem.endswith('_thumb'):
                continue
            # Aynı görselin WebP sürümü varsa yalnızca onu kaydet.
            if path.suffix.lower() != '.webp' and path.with_suffix('.webp').is_file():
                continue

            rel = f'{folder_name}/{path.name}'
            if rel in existing:
                continue
            model.objects.create(image=rel, title=_title(path), order=order)
            existing.add(rel)
            order += 1


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0004_sitecomment'),
    ]

    operations = [
        migrations.RunPython(seed_static_catalog_once, migrations.RunPython.noop),
    ]
