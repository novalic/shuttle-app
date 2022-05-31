import json
import redis

from django.contrib.gis.geos import Polygon
from django.db.models import QuerySet
from typing import Optional

from apps.parameters.models import WorldArea
from apps.utils import get_redis_client

from ..models import ServiceArea


def add_new_polygon_to_cache(service_area: ServiceArea, /, *, delete_polygon: Optional[Polygon] = None):
    redis_instance = get_redis_client()

    intersection_qs = WorldArea.objects.filter(square__intersects=service_area.polygon)

    if intersection_qs.exists():
        for area in intersection_qs:
            area_code = area.code

            value = redis_instance.get(area_code)
            if not value:
                value = list()
            else:
                value = json.loads(value)

            value.append(service_area.id)

            redis_instance.set(area.code, json.dumps(value))

    if delete_polygon:
        delete_polygon_from_cache(service_area, delete_polygon, redis_instance=redis_instance)


def delete_polygon_from_cache(
        service_area: ServiceArea,
        delete_polygon: Polygon,
        /,
        *,
        redis_instance: redis.StrictRedis = None):

    if not redis_instance:
        redis_instance = get_redis_client()

    intersection_qs = WorldArea.objects.filter(square__intersects=delete_polygon)

    for area in intersection_qs:
        area_code = area.code

        value = redis_instance.get(area_code)
        if not value:
            continue

        value = set(json.loads(value))
        try:
            value.remove(service_area.id)
        except KeyError:
            continue

        value = list(value)
        redis_instance.set(area.code, json.dumps(value))


def delete_polygon_batch_from_cache(service_areas: QuerySet):
    redis_instance = get_redis_client()

    for service_area in service_areas:
        delete_polygon_from_cache(service_area, service_area.polygon, redis_instance=redis_instance)
