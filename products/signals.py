from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = "product_list"
    cache.delete(cache_key)
