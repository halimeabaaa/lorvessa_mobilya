import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Render ortam değişkenlerinden superuser oluşturur veya şifresini günceller.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()
        if not username or not password:
            self.stdout.write('DJANGO_SUPERUSER_USERNAME / PASSWORD yok, atlandı.')
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        action = 'oluşturuldu' if created else 'güncellendi'
        self.stdout.write(self.style.SUCCESS(f'Superuser {action}: {username}'))
