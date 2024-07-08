from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Guest


@receiver(post_save, sender=Guest)
def invalidate_cache(sender, instance, **kwargs) -> None:
    cache.delete('guest_list')
