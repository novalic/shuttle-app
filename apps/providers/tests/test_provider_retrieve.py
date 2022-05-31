from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Provider


class ProvidersRetrieveTests(APITestCase):
    endpoint_name = 'provider-detail'

    @classmethod
    def setUpTestData(cls):
        super(ProvidersRetrieveTests, cls).setUpTestData()

        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        cls.provider = Provider.objects.create(**payload)

    def test_provider_retrieve_success(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id})

        response = self.client.get(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['id'], self.provider.id)

    def test_provider_retrieve_failure_does_not_exist(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id + 100})

        response = self.client.get(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
