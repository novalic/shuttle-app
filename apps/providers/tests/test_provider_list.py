from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Provider


class ProvidersUpdateTests(APITestCase):
    endpoint = reverse('provider-list')

    @classmethod
    def setUpTestData(cls):
        super(ProvidersUpdateTests, cls).setUpTestData()

        cls.provider = Provider.objects.create(**{
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        })
        cls.provider_two = Provider.objects.create(**{
            'currency': 'EUR',
            'email': 'user@email.com',
            'language': 'ES',
            'name': 'Test 2',
            'phone_number': '+34685065551'
        })

    def test_provider_list(self):
        response = self.client.get(
            self.endpoint
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        expected_ids = {self.provider.id, self.provider_two.id}

        self.assertEqual(response_data['count'], len(expected_ids))
        results = response_data['results']

        for provider in results:
            self.assertIn(provider['id'], expected_ids)
