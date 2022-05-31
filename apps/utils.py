import redis

from django.conf import settings


def get_redis_client() -> redis.StrictRedis:
    redis_client = redis.StrictRedis(
        host=settings.REDIS_HOSTNAME,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_NUMBER
    )
    return redis_client
