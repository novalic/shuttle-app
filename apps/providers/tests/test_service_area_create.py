from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ..models import Provider, ServiceArea


class ServiceAreaCreateTests(APITestCase):
    endpoint = reverse('service-area-list')

    @classmethod
    def setUpTestData(cls):
        super(ServiceAreaCreateTests, cls).setUpTestData()

        cls.payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        cls.provider = Provider.objects.create(**cls.payload)

    def setUp(self) -> None:
        super(ServiceAreaCreateTests, self).setUp()
        self.add_new_polygon_to_cache_mock = mock.patch('apps.providers.views.area.add_new_polygon_to_cache').start()
        self.add_new_polygon_to_cache_mock.return_value = True

    def tearDown(self) -> None:
        super(ServiceAreaCreateTests, self).tearDown()
        self.add_new_polygon_to_cache_mock.reset_mock()
        mock.patch.stopall()

    def test_service_area_create_success(self):
        payload = {
            'name': 'Test area',
            'price': 500.5,
            'provider': self.provider.id,
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        service_area_qs = ServiceArea.objects.all()

        self.assertEqual(service_area_qs.count(), 1)
        service_area_obj = service_area_qs.first()
        self.assertEqual(service_area_obj.provider_id, payload['provider'])
        self.assertEqual(service_area_obj.name, payload['name'])
        self.assertEqual(service_area_obj.price, payload['price'])
        self.assertEqual(service_area_obj.polygon.num_points, len(payload['polygon']))

        self.add_new_polygon_to_cache_mock.assert_called_once()

    # failure tests

    def test_service_area_create_failure_missing_required_field_name(self):
        payload = {
            'price': 500.5,
            'provider': self.provider.id,
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('name', response_data)
        self.assertEqual(response_data['name'][0], 'This field is required.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_create_failure_missing_required_field_price(self):
        payload = {
            'name': 'Test area',
            'provider': self.provider.id,
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('price', response_data)
        self.assertEqual(response_data['price'][0], 'This field is required.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_create_failure_missing_required_field_provider(self):
        payload = {
            'name': 'Test area',
            'price': 500.5,
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('provider', response_data)
        self.assertEqual(response_data['provider'][0], 'This field is required.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_create_failure_missing_required_field_polygon(self):
        payload = {
            'name': 'Test area',
            'price': 500.5,
            'provider': self.provider.id
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('polygon', response_data)
        self.assertEqual(response_data['polygon'][0], 'This field is required.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_create_failure_invalid_provider_type(self):
        payload = {
            'name': 'Test area',
            'price': 500.5,
            'provider': 'provider',
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('provider', response_data)
        self.assertEqual(response_data['provider'][0], 'Incorrect type. Expected pk value, received str.')

        self.add_new_polygon_to_cache_mock.assert_not_called()

    def test_service_area_create_failure_invalid_provider_id(self):
        invalid_id = self.provider.id + 100
        payload = {
            'name': 'Test area',
            'price': 500.5,
            'provider': invalid_id,
            'polygon': [[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('provider', response_data)
        self.assertEqual(response_data['provider'][0], f'Invalid pk "{invalid_id}" - object does not exist.')

        self.add_new_polygon_to_cache_mock.assert_not_called()
