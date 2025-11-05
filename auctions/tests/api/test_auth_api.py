import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import User

class TestLoginView:

    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.url = reverse('api-login')

    def test_login_successful(self, api_client, user):
        response = api_client.post(self.url, {
            "username": "testuser",
            "password": "12345"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "testuser" in response.data["user"]["username"]

    def test_login_invalid_credentials(self, api_client):
        response = api_client.post(self.url, {
            "username": "testuser",
            "password": "wrongpass"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data

    def test_login_missing_fields(self, api_client):
        response = api_client.post(self.url, {
            "username": "testuser"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

class TestLogOutView:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.url = reverse('api-logout')

    def test_logout_successful(self, authenticated_client):
        response = authenticated_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_without_being_logged_in(self, api_client):
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

class TestRegisterView:

    @pytest.fixture(autouse = True)
    def setup(self, db):
        self.url = reverse('api-register')
        self.user = {
            "username": "testuser",
            "password": "secret123",
            "email": "john@mail.com",
            "confirmation": "secret123"
        }

    def test_register_successful(self, api_client):
        response = api_client.post(self.url, self.user)

        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "testuser" in response.data["user"]["username"]
        assert User.objects.filter(username="testuser").exists()
        
        user = User.objects.get(username="testuser")
        assert user.check_password("secret123")
