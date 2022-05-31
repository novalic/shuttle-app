from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProvidersCreateTests(APITestCase):
    endpoint = reverse('provider-list')

    def test_providers_create_success(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        for field in payload.keys():
            self.assertIn(field, response_data)
            self.assertEqual(payload[field], response_data[field])

        self.assertIn('id', response_data)
        self.assertIn('timestamp', response_data)

    # failure tests

    def test_providers_create_failure_missing_field_currency(self):
        payload = {
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('currency', response_data)
        self.assertEqual(response_data['currency'][0], 'This field is required.')

    def test_providers_create_failure_missing_field_email(self):
        payload = {
            'currency': 'USD',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'][0], 'This field is required.')

    def test_providers_create_failure_missing_field_language(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('language', response_data)
        self.assertEqual(response_data['language'][0], 'This field is required.')

    def test_providers_create_failure_missing_field_name(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'phone_number': '+34685061901'
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

    def test_providers_create_failure_missing_field_phone_number(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('phone_number', response_data)
        self.assertEqual(response_data['phone_number'][0], 'This field is required.')

    def test_providers_create_failure_invalid_currency(self):
        payload = {
            'currency': '55',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('currency', response_data)
        self.assertEqual(response_data['currency'][0], f'Invalid value for currency: {payload["currency"]}.')

    def test_providers_create_failure_invalid_email(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolasemail.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'][0], 'Enter a valid email address.')

    def test_providers_create_failure_invalid_language(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'T',
            'name': 'Test',
            'phone_number': '+34685061901'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('language', response_data)
        self.assertEqual(response_data['language'][0], f'Invalid value for language: {payload["language"]}.')

    def test_providers_create_failure_invalid_phone_number(self):
        payload = {
            'currency': 'USD',
            'email': 'nicolas@email.com',
            'language': 'EN',
            'name': 'Test',
            'phone_number': 'invalid_phone'
        }

        response = self.client.post(
            self.endpoint,
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()

        self.assertIn('phone_number', response_data)
        self.assertEqual(response_data['phone_number'][0], 'The phone number entered is not valid.')
