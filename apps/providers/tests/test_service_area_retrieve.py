from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Provider, ServiceArea


class ServiceAreaRetrieveTests(APITestCase):
    endpoint_name = 'service-area-detail'

    @classmethod
    def setUpTestData(cls):
        super(ServiceAreaRetrieveTests, cls).setUpTestData()

        cls.provider = Provider.objects.create(**{
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        })

        cls.service_area = ServiceArea.objects.create(
            polygon=Polygon([[0.0, 0.0], [0.0, 50.0], [50.0, 50.0], [50.0, 0.0], [0.0, 0.0]]),
            provider_id=cls.provider.id,
            price=500.5,
            name='Test area'
        )

    def test_service_area_retrieve_success(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.service_area.id})

        response = self.client.get(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data['id'], self.service_area.id)

    def test_service_area_retrieve_failure_invalid_id(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.service_area.id + 100})

        response = self.client.get(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
