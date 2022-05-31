import json

from apps.providers.models import ServiceArea
from apps.utils import get_redis_client

from ..models import WorldArea


def populate_cache():
    redis_instance = get_redis_client()

    for service_area in ServiceArea.objects.all():
        intersection_qs = WorldArea.objects.filter(square__intersects=service_area.polygon)

        if not intersection_qs.exists():
            continue

        for area in intersection_qs:
            area_code = area.code

            value = redis_instance.get(area_code)
            if not value:
                value = list()
            else:
                value = json.loads(value)

            value.append(service_area.id)

            redis_instance.set(area.code, json.dumps(value))
