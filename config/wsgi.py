import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

try:
    call_command('migrate', interactive=False, verbosity=1)
    call_command('ensure_superuser', verbosity=1)
    call_command('seed_media_catalog', verbosity=1)
except Exception as exc:
    print(f'WSGI boot error: {exc}', flush=True)
