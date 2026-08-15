from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path

from pages.image_utils import ensure_optimized, optimize_file
from pages.models import GalleryItem, SliderImage


class Command(BaseCommand):
    help = 'Medya görsellerini WebP + thumbnail olarak optimize eder (sayfa hızı).'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Var olan WebP dosyalarını yeniden üret')

    def handle(self, *args, **options):
        force = options['force']
        created = 0
        paths = set()

        for obj in GalleryItem.objects.exclude(image=''):
            if obj.image:
                name = obj.image.name.replace('\\', '/')
                if name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    paths.add(name)
        for obj in SliderImage.objects.exclude(image='').exclude(image=None):
            if obj.image:
                name = obj.image.name.replace('\\', '/')
                if name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    paths.add(name)

        media_root = Path(settings.MEDIA_ROOT)
        for folder in ('gallery', 'slider'):
            d = media_root / folder
            if d.is_dir():
                for f in d.iterdir():
                    if f.is_file() and f.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                        rel = str(f.relative_to(media_root)).replace('\\', '/')
                        paths.add(rel)

        self.stdout.write(f'{len(paths)} görsel işlenecek…')
        for rel in sorted(paths):
            result = ensure_optimized(rel, force=force)
            if result['created']:
                created += len(result['created'])
                self.stdout.write(self.style.SUCCESS(f'  + {rel}'))
            else:
                self.stdout.write(f'  · {rel} (hazır)')

        static_img = Path(settings.BASE_DIR) / 'static' / 'img' / 'lorvessa-emblem.png'
        if static_img.is_file():
            dest = static_img.with_suffix('.webp')
            if force or not dest.is_file():
                if optimize_file(static_img, dest, 256, 80):
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'  + emblem -> {dest.name}'))

        self.stdout.write(self.style.SUCCESS(f'Tamam: {created} yeni dosya üretildi.'))
