import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import User
from django.utils import timezone

class TestSoftDeleteUserAPI:
    @pytest.fixture(autouse=True)
    def setUp(self, db, user):
        self.url = reverse("api-softDeleteUser")
        self.body = {
            "confirm": True,
            "reason": "User deleted for test purpouses"
            }

    # Z - Zero
    def test_soft_delete_with_empty_json(self, authenticated_client):
        response = authenticated_client.post(self.url, {}) # Without confirm
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_soft_delete_without_reason(self, authenticated_client):
        response = authenticated_client.post(self.url, {"confirm": True})
        assert response.status_code == status.HTTP_400_BAD_REQUEST # falta razao pelo delete
        
    # O - One
    def test_soft_delete_own_account_with_valid_confirm(self, user, authenticated_client):
        response = authenticated_client.post(self.url, self.body)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db() # Verificar no banco
        assert user.deleted_at is not None
        assert user.deleted_reason is not None
        assert user.is_active is False

    # M - Many
    def test_soft_delete_own_account_multiple_times_idempotent(self, user, authenticated_client):
        original_time = timezone.now() - timezone.timedelta(days=1)
        user.deleted_at = original_time
        user.is_active = False
        user.save()

        response = authenticated_client.post(self.url, self.body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Usuário já deletado

        user.refresh_from_db() # Verificar no banco
        assert user.deleted_at is not None
        assert user.deleted_at == original_time  # O timestamp NÃO muda!
        assert user.is_active is False

    # B - Boundary
    def test_soft_delete_with_reason_at_minimum_length(self, user, authenticated_client): # deve conter 10 caracteres
        response = authenticated_client.post(self.url, {"confirm": True, "reason": "1234567890"})
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db() # Verificar no banco
        assert user.is_active is False

    # E - Exceptions
    def test_soft_delete_without_authentication(self, api_client, user):
        response = api_client.post(self.url, self.body)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        user.refresh_from_db() # Verificar no banco
        assert user.is_active is True


    def test_soft_delete_without_confirm_field(self, user, authenticated_client):
        response = authenticated_client.post(self.url, {"reason": "1234567890"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db() # Verificar no banco
        assert user.is_active is True

    def test_soft_delete_with_confirm_false(self, user, authenticated_client):
        response = authenticated_client.post(self.url, {"confirm": False, "reason": "1234567890"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db() # Verificar no banco
        assert user.is_active is True

    def test_soft_delete_with_too_short_reason(self, authenticated_client, user):
        response = authenticated_client.post(self.url, {"confirm": True, "reason": "1234567"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db() # Verificar no banco
        assert user.is_active is True
