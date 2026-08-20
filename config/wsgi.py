import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()


def _prepare_render_media():
    """Git'teki media/ klasörünü /tmp'ye kopyala (Render'da kalıcı disk yok)."""
    if not os.environ.get('RENDER'):
        return
    dest = Path(settings.MEDIA_ROOT)
    src = Path(settings.BASE_DIR) / 'media'
    dest.mkdir(parents=True, exist_ok=True)
    marker = dest / '.seeded'
    if marker.exists():
        print(f'Render media already seeded at {dest}', flush=True)
        return
    if src.is_dir():
        file_count = sum(1 for p in src.rglob('*') if p.is_file())
        print(f'Seeding Render media from {src} ({file_count} files) -> {dest}', flush=True)
        shutil.copytree(src, dest, dirs_exist_ok=True)
        marker.write_text('ok', encoding='utf-8')
    else:
        print(f'WARNING: source media missing at {src}', flush=True)


try:
    _prepare_render_media()
    call_command('migrate', interactive=False, verbosity=1)
    call_command('ensure_superuser', verbosity=1)
    call_command('seed_media_catalog', verbosity=1)
except Exception as exc:
    print(f'WSGI boot error: {exc}', flush=True)
