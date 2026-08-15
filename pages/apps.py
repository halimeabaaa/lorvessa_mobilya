import sys

from django.apps import AppConfig


def _patch_django_context_for_python314():
    """Python 3.14'te copy(super()) kırıldığı için Django BaseContext.__copy__ yaması.

    Bkz. https://code.djangoproject.com/ticket/35844
    """
    if sys.version_info < (3, 14):
        return

    from copy import copy

    from django.template.context import BaseContext

    def __copy__(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__ = copy(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = __copy__


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Site içeriği'

    def ready(self):
        _patch_django_context_for_python314()
        from . import signals  # noqa: F401
