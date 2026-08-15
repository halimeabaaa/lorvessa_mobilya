from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GalleryItem, SliderImage
from .image_utils import ensure_optimized, relative_media_path


def _optimize_field(file_field):
    rel = relative_media_path(file_field)
    if rel and not rel.lower().endswith('.webp'):
        ensure_optimized(rel, force=False)


@receiver(post_save, sender=GalleryItem)
def optimize_gallery_image(sender, instance, **kwargs):
    if instance.image:
        _optimize_field(instance.image)


@receiver(post_save, sender=SliderImage)
def optimize_slider_image(sender, instance, **kwargs):
    if instance.image:
        _optimize_field(instance.image)
