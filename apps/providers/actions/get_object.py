import json
import redis

from typing import Union, Set

from apps.utils import get_redis_client


def get_object_from_cache(cache_key: str, /, *, redis_instance: redis.StrictRedis = None) -> Union[Set[int], list]:
    if not redis_instance:
        redis_instance = get_redis_client()

    value = redis_instance.get(cache_key)
    if not value:
        return []

    return set(json.loads(value))
