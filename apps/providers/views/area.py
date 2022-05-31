from rest_framework import status

from django.contrib.gis.geos import Polygon
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..actions.update_cache import add_new_polygon_to_cache, delete_polygon_from_cache
from ..models import ServiceArea
from ..serializers import AreaValidationSerializer, ServiceAreaSerializer, AreaUpdateValidationSerializer


class ServiceAreaViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def create_service_area(self, request, *args, **kwargs):
        payload = request.data

        serializer = AreaValidationSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        service_area_obj = ServiceArea.objects.create(
            name=payload.get('name'),
            price=payload.get('price'),
            polygon=Polygon(payload.get('polygon')),
            provider_id=payload.get('provider')
        )

        add_new_polygon_to_cache(service_area_obj)

        return Response(status=status.HTTP_201_CREATED)

    def update_service_area(self, request, *args, **kwargs):
        service_area_obj = self.get_object()

        payload = request.data

        serializer = AreaUpdateValidationSerializer(
            data=payload,
            context={'area_provider_id': service_area_obj.provider_id}
        )
        serializer.is_valid(raise_exception=True)

        old_polygon = service_area_obj.polygon

        _ = ServiceArea.objects.filter(id=service_area_obj.id).update(
            name=payload.get('name'),
            price=payload.get('price'),
            polygon=Polygon(payload.get('polygon'))
        )

        service_area_obj.refresh_from_db()
        add_new_polygon_to_cache(service_area_obj, delete_polygon=old_polygon)

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        service_area_obj = self.get_object()
        delete_polygon_from_cache(service_area_obj, service_area_obj.polygon)
        return super(ServiceAreaViewSet, self).destroy(request)
