from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Provider


class ProvidersUpdateTests(APITestCase):
    endpoint_name = 'provider-detail'

    @classmethod
    def setUpTestData(cls):
        super(ProvidersUpdateTests, cls).setUpTestData()

        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        cls.provider = Provider.objects.create(**payload)

    def test_provider_update_success(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id})

        payload = {
            'currency': 'EUR',
            'email': 'user@email.com',
            'language': 'ES',
            'name': 'Test 2',
            'phone_number': '+34685061111'
        }
        response = self.client.put(
            endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        for field in payload.keys():
            self.assertEqual(payload[field], response_data[field])

    def test_provider_update_failure_does_not_exist(self):
        endpoint = reverse(self.endpoint_name, kwargs={'pk': self.provider.id + 100})

        response = self.client.put(
            endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
