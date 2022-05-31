from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ..models import Provider, ServiceArea


class ServiceAreaUpdateTests(APITestCase):
    endpoint_name = 'service-area-detail'

    @classmethod
    def setUpTestData(cls):
        super(ServiceAreaUpdateTests, cls).setUpTestData()

        cls.provider = Provider.objects.create(**{
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        })

        cls.another_provider = Provider.objects.create(**{
            'currency': 'USD',
            'email': 'another@email.com',
            'language': 'SP',
            'name': 'Test 2',
            'phone_number': '+34685061456'
        })

        cls.service_area = ServiceArea.objects.create(
            polygon=Polygon([[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]),
            provider_id=cls.provider.id,
            price=500.5,
            name='Test area'
        )

    def setUp(self) -> None:
        super(ServiceAreaUpdateTests, self).setUp()
        self.add_new_polygon_to_cache_mock = mock.patch('apps.providers.views.area.add_new_polygon_to_cache').start()
        self.add_new_polygon_to_cache_mock.return_value = True

    def tearDown(self) -> None:
        super(ServiceAreaUpdateTests, self).tearDown()
        self.add_new_polygon_to_cache_mock.reset_mock()
        mock.patch.stopall()

    # NOTE ---- Failure tests related to serializer validation are done in the create test class and not repeated here

    def test_service_area_update_success(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.service_area.id})

        payload = {
            'name': 'Test area 2',
            'price': 12.5,
            'provider': self.provider.id,
            'polygon': [[50.0, 50.0], [50.0, 100.0], [100.0, 100.0], [100.0, 50.0], [50.0, 50.0]]
        }

        response = self.client.put(
            endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.service_area.refresh_from_db()

        self.assertEqual(self.service_area.name, payload['name'])
        self.assertEqual(self.service_area.price, payload['price'])
        self.assertEqual(self.service_area.provider_id, self.provider.id)

        self.add_new_polygon_to_cache_mock.assert_called_once()

    def test_service_area_update_failure_provider_does_not_match(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.service_area.id})

        payload = {
            'name': 'Test area 2',
            'price': 12.5,
            'provider': self.another_provider.id,
            'polygon': [[50.0, 50.0], [50.0, 100.0], [100.0, 100.0], [100.0, 50.0], [50.0, 50.0]]
        }

        response = self.client.put(
            endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('provider', response_data)
        self.assertEqual(response_data['provider'][0], 'Provider does not match.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_update_failure_not_found(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.service_area.id + 100})

        payload = {
            'name': 'Test area 2',
            'price': 12.5,
            'provider': self.another_provider.id,
            'polygon': [[50.0, 50.0], [50.0, 100.0], [100.0, 100.0], [100.0, 50.0], [50.0, 50.0]]
        }

        response = self.client.put(
            endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.add_new_polygon_to_cache_mock.assert_not_called()
