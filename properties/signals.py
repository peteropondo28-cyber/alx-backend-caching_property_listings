from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
@receiver(post_delete, sender=Property)
def clear_property_cache(sender, **kwargs):
    cache.delete('all_properties')
