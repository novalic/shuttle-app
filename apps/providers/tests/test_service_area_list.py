from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Provider, ServiceArea


class ServiceAreaCreateTests(APITestCase):
    endpoint = reverse('service-area-list')

    @classmethod
    def setUpTestData(cls):
        super(ServiceAreaCreateTests, cls).setUpTestData()

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
        cls.another_service_area = ServiceArea.objects.create(
            polygon=Polygon([[50.0, 50.0], [50.0, 100.0], [100.0, 100.0], [100.0, 50.0], [50.0, 50.0]]),
            provider_id=cls.another_provider.id,
            price=85.5,
            name='Test area 2'
        )

    def test_service_area_list(self):
        response = self.client.get(
            self.endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        expected_ids = {self.service_area.id, self.another_service_area.id}

        self.assertEqual(response_data['count'], len(expected_ids))
        results = response_data['results']

        for result in results:
            self.assertIn(result['id'], expected_ids)
