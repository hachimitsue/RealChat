from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile

class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        print(response.json())  # Print the response data to debug the issue
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.json())

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        # No need to create Profile manually as it is created by the signal
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())