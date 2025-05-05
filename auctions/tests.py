from django.test import TestCase

from rest_framework.test import APITestCase
from .models import User
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class TestLoginView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret123")
        self.url = reverse('api-login')

    def test_login_successful(self):
        response = self.client.post(self.url, {
            "username": "john",
            "password": "secret123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data) #Por que é preciso verificar isto?
        self.assertEqual(response.data["user"]["username"], "john")

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            "username": "john",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_missing_fields(self):
            response = self.client.post(self.url, {
            "username": "john"
        })
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("password", response.data)