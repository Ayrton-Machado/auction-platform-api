import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import User
from django.utils import timezone

class TestLoginView: #Zombies

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

class TestRegisterView: #Zombies

    @pytest.fixture(autouse = True)
    def setup(self, db):
        self.url = reverse('api-register')
        self.user = {
            "username": "testuser",
            "password": "secret123",
            "email": "john@mail.com",
            "confirmation": "secret123"
        }

    # Zero Cases
    def test_register_missing_username(self, api_client):
        user_missing_username = self.user.copy()
        user_missing_username["username"] = ""
        response = api_client.post(self.url, user_missing_username)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_register_missing_password(self, api_client):
        user_missing_password = self.user.copy()
        user_missing_password["password"] = ""
        response = api_client.post(self.url, user_missing_password)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_register_missing_email(self, api_client):
        user_missing_email = self.user.copy()
        user_missing_email["email"] = ""
        response = api_client.post(self.url, user_missing_email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_missing_confirmation(self, api_client):
        user_missing_confirmation = self.user.copy()
        user_missing_confirmation["confirmation"] = ""
        response = api_client.post(self.url, user_missing_confirmation)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_empty_username(self, api_client):
        user_empty_username = self.user.copy()
        del user_empty_username["username"]
        response = api_client.post(self.url, user_empty_username)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_register_empty_password(self, api_client):
        user_empty_password = self.user.copy()
        del user_empty_password["password"]
        response = api_client.post(self.url, user_empty_password)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_register_empty_email(self, api_client):
        user_empty_email = self.user.copy()
        del user_empty_email["email"]
        response = api_client.post(self.url, user_empty_email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_empty_confirmation(self, api_client):
        user_empty_confirmation = self.user.copy()
        del user_empty_confirmation["confirmation"]
        response = api_client.post(self.url, user_empty_confirmation)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'confirmation' in response.data


    def test_register_empty_payload(self, api_client):
        response = api_client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # One Cases
    def test_register_successful(self, api_client):
        response = api_client.post(self.url, self.user)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="testuser").exists()
        assert "user" in response.data
        assert "testuser" in response.data["user"]["username"]

        user = User.objects.get(username="testuser")

        assert user.created_at is not None
        assert user.deleted_at is None
        assert user.check_password("secret123")

    def test_register_sets_created_at(self, api_client):
        """Testa se created_at é definido automaticamente no registro"""
        before_creation = timezone.now()
        
        response = api_client.post(self.url, {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "securepass123",
            "confirmation": "securepass123"
        })
        
        after_creation = timezone.now()
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar no banco
        user = User.objects.get(username="newuser")
        assert user.created_at is not None
        assert before_creation <= user.created_at <= after_creation

    def test_register_password_mismatch(self, api_client):
        user_mismatch_password = self.user.copy()
        user_mismatch_password["confirmation"] = "secrt123"
        response = api_client.post(self.url, user_mismatch_password)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Já testa email duplicado (case-insensitive)
    def test_register_case_insensitive_email(self, api_client):
        response = api_client.post(self.url, self.user) # Cria primeiro usuário

        assert response.status_code == status.HTTP_201_CREATED # Verifica criação para não haver aprovação com erro fantasma

        user_email_case_insensitive = self.user.copy()
        user_email_case_insensitive["username"] = "newuser"
        user_email_case_insensitive["email"] = "JohN@mail.com"

        response = api_client.post(self.url, user_email_case_insensitive) # Tenta criar com email ja existente

        assert response.status_code == status.HTTP_400_BAD_REQUEST # Case insensitive recusa diferenciacao por letras maiusculas e minusculas
    
    # Já testa username duplicado (case-insensitive)
    def test_register_case_insensitive_user(self, api_client):
        response = api_client.post(self.url, self.user) # Cria primeiro usuário

        assert response.status_code == status.HTTP_201_CREATED # Verifica criação para não haver aprovação com erro fantasma

        user_username_case_insensitive = self.user.copy()
        user_username_case_insensitive["username"] = "TestUser"
        user_username_case_insensitive["email"] = "newuser@mail.com"

        response = api_client.post(self.url, user_username_case_insensitive)

        assert response.status_code == status.HTTP_400_BAD_REQUEST # Case insensitive recusa diferenciacao por letras maiusculas e minusculas
    
    # Boundary Cases
    def test_register_invalid_email_format(self, api_client):
        user_invalid_email_format = self.user.copy()
        user_invalid_email_format["email"] = "testuser.com" # Email sem @

        response = api_client.post(self.url, user_invalid_email_format)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_username_min_length(self, api_client):
        user_invalid_username_length = self.user.copy()
        user_invalid_username_length["username"] = "te" # Minimo permitido é 3 caracteres

        response = api_client.post(self.url, user_invalid_username_length)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_username_max_length(self, api_client):
        user_invalid_username_length = self.user.copy()
        # Maximo permitido é 150 pelo django user
        user_invalid_username_length["username"] = "test_user_case_insensitive_example_account_with_really_long_name_for_edge_case_validation_checking_purpose_abcdefghijklmno1234567890_xyz"

        response = api_client.post(self.url, user_invalid_username_length)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_min_length(self, api_client):
        user_invalid_password_length = self.user.copy()
        user_invalid_password_length["password"] = "1234567" # Minimo permitido é 8 caracteres

        response = api_client.post(self.url, user_invalid_password_length)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Interface Cases
    def test_register_returns_user_data(self, api_client):
        """Verificar estrutura da resposta após POST bem-sucedido"""
        response = api_client.post(self.url, self.user)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verifica estrutura do response.data
        assert "user" in response.data
        assert "username" in response.data["user"]
        assert "email" in response.data["user"]
        assert response.data["user"]["username"] == "testuser"
        assert response.data["user"]["email"] == "john@mail.com"

    def test_register_does_not_return_password(self, api_client):
        """Garantir que senha não é retornada no response"""
        response = api_client.post(self.url, self.user)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data.get("user", {})
        assert "confirmation" not in response.data.get("user", {})

    # Exceptions Cases
    def test_register_sql_injection_attempt(self, api_client):
        user_sql_injection = self.user.copy()
        user_sql_injection["username"] = "admin' --"

        response = api_client.post(self.url, user_sql_injection)

        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST] # Dupla camada de verificação, caso django falhe

        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username="admin' --")
            assert user.username == "admin' --" # Dupla camada de verificação, caso django falhe

    def test_register_xss_attempt(self, api_client):
        user_xss = self.user.copy()
        user_xss["username"] = "<script>alert('xss')</script>"

        response = api_client.post(self.url, user_xss)

        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST] # Dupla camada de verificação, caso django falhe

        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username="<script>alert('xss')</script>")
            assert user.username == "<script>alert('xss')</script>" # Dupla camada de verificação, caso django falhe

    # Simple Cases
    def test_register_with_extra_fields(self, api_client):
        """Payload com campos extras que devem ser ignorados"""
        user_with_extra_fields = self.user.copy()
        # Adiciona campos que NÃO fazem parte do modelo User
        user_with_extra_fields["is_admin"] = True  # Campo perigoso!
        user_with_extra_fields["is_staff"] = True
        user_with_extra_fields["is_superuser"] = True
        user_with_extra_fields["random_field"] = "malicious_data"
        user_with_extra_fields["id"] = 999
        
        response = api_client.post(self.url, user_with_extra_fields)
        
        # Deve criar o usuário normalmente, ignorando campos extras
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verificar que campos extras foram IGNORADOS
        user = User.objects.get(username="testuser")
        assert user.is_staff == False  # Não foi promovido a staff!
        assert user.is_superuser == False  # Não virou superuser!
        assert user.username == "testuser"
        assert user.email == "john@mail.com"
        
        # Garantir que campos extras não aparecem na resposta
        assert "random_field" not in response.data.get("user", {})
        assert "is_admin" not in response.data.get("user", {})