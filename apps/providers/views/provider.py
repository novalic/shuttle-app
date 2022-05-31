from rest_framework.viewsets import ModelViewSet

from ..actions.update_cache import delete_polygon_batch_from_cache
from ..models import Provider, ServiceArea
from ..serializers import ProviderSerializer


class ProvidersViewSet(ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    def destroy(self, request, *args, **kwargs):
        provider_id = kwargs['pk']

        service_area_qs = ServiceArea.objects.filter(provider_id=provider_id)

        if service_area_qs.exists():
            delete_polygon_batch_from_cache(service_area_qs)
            _ = service_area_qs.delete()

        return super(ProvidersViewSet, self).destroy(request)
