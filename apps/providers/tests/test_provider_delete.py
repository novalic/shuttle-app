from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ..models import Provider, ServiceArea


class ProvidersDeleteTests(APITestCase):
    endpoint_name = 'provider-detail'

    @classmethod
    def setUpTestData(cls):
        super(ProvidersDeleteTests, cls).setUpTestData()

        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        cls.provider = Provider.objects.create(**payload)

        cls.service_area = ServiceArea.objects.create(
            polygon=Polygon([[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]),
            provider_id=cls.provider.id,
            price=500.5,
            name='Test area'
        )

    def setUp(self) -> None:
        super(ProvidersDeleteTests, self).setUp()
        self.delete_polygon_batch_from_cache_mock = mock.patch(
            'apps.providers.views.provider.delete_polygon_batch_from_cache'
        ).start()
        self.delete_polygon_batch_from_cache_mock.return_value = True

    def tearDown(self) -> None:
        super(ProvidersDeleteTests, self).tearDown()
        self.delete_polygon_batch_from_cache_mock.reset_mock()
        mock.patch.stopall()

    def test_provider_delete_success(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id})

        provider_id = self.provider.id
        service_area_id = self.service_area.id

        response = self.client.delete(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Provider.objects.filter(pk=provider_id).exists())
        self.assertFalse(ServiceArea.objects.filter(pk=service_area_id).exists())

        self.delete_polygon_batch_from_cache_mock.assert_called_once()

    def test_provider_delete_failure_does_not_exist(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id + 100})

        response = self.client.delete(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.delete_polygon_batch_from_cache_mock.assert_not_called()
