from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from ..models import Provider, ServiceArea


class FindServiceAreaCreateTests(APITestCase):
    endpoint = reverse('find-service-area')

    @classmethod
    def setUpTestData(cls):
        super(FindServiceAreaCreateTests, cls).setUpTestData()

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
        cls.last_provider = Provider.objects.create(**{
            'currency': 'USD',
            'email': 'last@email.com',
            'language': 'FR',
            'name': 'Test 3',
            'phone_number': '+34685061776'
        })

        cls.service_area = ServiceArea.objects.create(
            polygon=Polygon([[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]),
            provider_id=cls.provider.id,
            price=500.5,
            name='Test area'
        )
        cls.another_service_area = ServiceArea.objects.create(
            polygon=Polygon([[50.0, 50.0], [50.0, 100.0], [100.0, 100.0], [100.0, 50.0], [50.0, 50.0]]),
            provider_id=cls.another_provider.id,
            price=85.5,
            name='Test area 2'
        )
        cls.last_service_area = ServiceArea.objects.create(
            polygon=Polygon([[75.0, 50.0], [75.0, 75.0], [100.0, 75.0], [100.0, 50.0], [75.0, 50.0]]),
            provider_id=cls.last_provider.id,
            price=5.2,
            name='Test area 2'
        )

    def setUp(self) -> None:
        super(FindServiceAreaCreateTests, self).setUp()
        self.get_object_from_cache_mock = mock.patch(
            'apps.providers.views.find_service_area.get_object_from_cache'
        ).start()
        self.get_object_from_cache_mock.return_value = True

    def tearDown(self) -> None:
        super(FindServiceAreaCreateTests, self).tearDown()
        self.get_object_from_cache_mock.reset_mock()
        mock.patch.stopall()

    def test_find_service_area_case_one_result(self):
        self.get_object_from_cache_mock.return_value = {self.service_area.id}

        querystring = '?latitude=25.0&longitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data['count'], 1)
        self.assertEqual(response_data['results'][0]['id'], self.service_area.id)

        self.get_object_from_cache_mock.assert_called_once()

    def test_find_service_area_case_boundary_zero_results(self):
        self.get_object_from_cache_mock.return_value = []

        querystring = '?latitude=50.0&longitude=50.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data['count'], 0)

        self.get_object_from_cache_mock.assert_called_once()

    def test_find_service_area_case_outside_zero_results(self):
        self.get_object_from_cache_mock.return_value = []

        querystring = '?latitude=-40.0&longitude=0.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data['count'], 0)

        self.get_object_from_cache_mock.assert_called_once()

    def test_find_service_area_case_inside_two_results(self):
        self.get_object_from_cache_mock.return_value = {self.another_service_area.id, self.last_service_area.id}

        querystring = '?latitude=80.0&longitude=60.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        expected_ids = {self.another_service_area.id, self.last_service_area.id}

        self.assertEqual(response_data['count'], len(expected_ids))

        for result in response_data['results']:
            self.assertIn(result['id'], expected_ids)

        self.get_object_from_cache_mock.assert_called_once()

    # failure tests

    def test_find_service_area_failure_missing_latitude(self):
        querystring = '?longitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('latitude', response_data)
        self.assertEqual(response_data['latitude'], 'Invalid value: None.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_missing_longitude(self):
        querystring = '?latitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('longitude', response_data)
        self.assertEqual(response_data['longitude'], 'Invalid value: None.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_value_for_latitude(self):
        invalid_value = 'aa'
        querystring = f'?latitude={invalid_value}&longitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('latitude', response_data)
        self.assertEqual(response_data['latitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_latitude_lower(self):
        invalid_value = -94.1235
        querystring = f'?latitude={invalid_value}&longitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('latitude', response_data)
        self.assertEqual(response_data['latitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_latitude_greater(self):
        invalid_value = 90.1235
        querystring = f'?latitude={invalid_value}&longitude=25.0'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('latitude', response_data)
        self.assertEqual(response_data['latitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_value_for_longitude(self):
        invalid_value = 'aa'
        querystring = f'?latitude=25.0&longitude={invalid_value}'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('longitude', response_data)
        self.assertEqual(response_data['longitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_longitude_lower(self):
        invalid_value = -200.0123
        querystring = f'?latitude=25.0&longitude={invalid_value}'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('longitude', response_data)
        self.assertEqual(response_data['longitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()

    def test_find_service_area_failure_invalid_longitude_greater(self):
        invalid_value = 190.0123
        querystring = f'?latitude=25.0&longitude={invalid_value}'

        response = self.client.get(
            self.endpoint + querystring
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('longitude', response_data)
        self.assertEqual(response_data['longitude'], f'Invalid value: {invalid_value}.')

        self.get_object_from_cache_mock.assert_not_called()
