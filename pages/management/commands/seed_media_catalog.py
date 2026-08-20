from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from pages.models import GalleryItem, SliderImage


class Command(BaseCommand):
    help = 'media/ klasöründeki görsellerden galeri/slider kayıtları oluşturur; eksik dosyalı kayıtları temizler.'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        self._purge_missing(GalleryItem, media_root)
        self._purge_missing(SliderImage, media_root)
        self._sync_folder(media_root / 'gallery', GalleryItem, 'gallery')
        self._sync_folder(media_root / 'slider', SliderImage, 'slider')

    def _purge_missing(self, model, media_root: Path):
        removed = 0
        for obj in model.objects.exclude(image='').only('id', 'image'):
            rel = (obj.image.name or '').replace('\\', '/')
            if not rel:
                continue
            if not (media_root / rel).is_file():
                obj.delete()
                removed += 1
        if removed:
            self.stdout.write(f'{model.__name__}: {removed} eksik dosyalı kayıt silindi')

    def _sync_folder(self, folder: Path, model, upload_prefix: str):
        if not folder.is_dir():
            self.stdout.write(f'Atlandı (yok): {folder}')
            return

        existing = {
            (obj.image.name or '').replace('\\', '/')
            for obj in model.objects.exclude(image='').only('image')
        }
        order = model.objects.count()
        created = 0

        files = sorted(folder.iterdir(), key=lambda p: p.name.lower())
        for path in files:
            if not path.is_file():
                continue
            name = path.name
            lower = name.lower()
            if lower.endswith('_thumb.webp'):
                continue
            if not lower.endswith(('.webp', '.png', '.jpg', '.jpeg')):
                continue
            if lower.endswith(('.png', '.jpg', '.jpeg')):
                webp = path.with_suffix('.webp')
                if webp.is_file():
                    continue

            rel = f'{upload_prefix}/{name}'.replace('\\', '/')
            if rel in existing:
                continue
            stem = path.stem.replace('_', ' ').strip() or name
            title = ' '.join(part.capitalize() for part in stem.split())
            model.objects.create(image=rel, title=title, order=order)
            existing.add(rel)
            order += 1
            created += 1

        self.stdout.write(self.style.SUCCESS(f'{model.__name__}: {created} kayıt eklendi'))
