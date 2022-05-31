from rest_framework import status

from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from typing import Optional, Tuple

from ..actions.get_object import get_object_from_cache
from ..models import ServiceArea
from ..serializers import ServiceAreaSerializer


class FindServiceAreaView(GenericViewSet):

    serializer_class = ServiceAreaSerializer

    def validate_querystring(self, latitude: Optional[str], longitude: Optional[str]) -> Optional[Tuple[float, float]]:
        try:
            lat = float(latitude)
        except (TypeError, ValueError):
            raise ValidationError({'latitude': f'Invalid value: {latitude}.'})

        if lat < -90 or lat > 90:
            raise ValidationError({'latitude': f'Invalid value: {lat}.'})

        try:
            lng = float(longitude)
        except (TypeError, ValueError):
            raise ValidationError({'longitude': f'Invalid value: {longitude}.'})

        if lng < -180 or lng > 180:
            raise ValidationError({'longitude': f'Invalid value: {lng}.'})

        return lat, lng

    def generate_cache_key(self, latitude, longitude):
        latitude = int(latitude)
        if latitude < 0:
            latitude -= latitude

        longitude = int(longitude)
        if longitude < 0:
            longitude -= 1

        return f'{latitude}_{longitude}'

    def find_service_areas(self, request, *args, **kwargs):
        query_parameters = self.request.query_params

        latitude = query_parameters.get('latitude')
        longitude = query_parameters.get('longitude')

        validated_coordinates = self.validate_querystring(latitude, longitude)

        cache_key = self.generate_cache_key(*validated_coordinates)
        service_area_ids = get_object_from_cache(cache_key)
        point = Point(validated_coordinates)

        cache_failure = False  # TODO: Implement a check to activate fallback system

        if cache_failure:
            service_area_qs = ServiceArea.objects.filter(polygon__contains=point)
        else:
            service_area_qs = ServiceArea.objects.filter(id__in=service_area_ids).filter(polygon__contains=point)

        page = self.paginate_queryset(service_area_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(service_area_qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
