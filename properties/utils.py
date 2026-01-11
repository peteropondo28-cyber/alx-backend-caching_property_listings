from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties from cache if available, 
    otherwise fetch from database and cache for 1 hour.
    """
    properties = cache.get('all_properties')
    if not properties:
        try:
            properties = list(Property.objects.all())
            cache.set('all_properties', properties, 3600)  # 1 hour
        except Exception as e:
            logger.error(f"Error fetching properties: {e}")
            properties = []
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Logs errors if Redis connection fails.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info('stats')
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Failed to retrieve Redis metrics: {e}")
        return {'hits': 0, 'misses': 0, 'hit_ratio': 0}
