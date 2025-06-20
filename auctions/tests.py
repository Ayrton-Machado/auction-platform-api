from django.test import TestCase

from rest_framework.test import APITestCase
from .models import *
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

class TestLogOutView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pedro", password="secret123")
        self.url = reverse('api-logout')
        self.client.login(username="pedro", password="secret123")

    def test_logout_successful(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Log Out Successful")

    def test_logout_without_being_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

class TestRegisterView(APITestCase):
    def setUp(self):
        self.url = reverse('api-register')

    def test_register_successful(self):
        #simula um register
        response = self.client.post(self.url, {
            "username": "john",
            "password": "secret123",
            "email": "john@mail.com", 
            "confirmation": "secret123"
        })
        #Verifica se a função está retornando o status correto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #Verifica se a função está retornando o user
        self.assertIn("user", response.data)
        #Verifica se a função está retornando o user correto
        self.assertEqual(response.data["user"]["username"], "john")
        #Verifica se foi corretamente criado no db
        self.assertTrue(User.objects.filter(username="john").exists())
        #Verifica se a senha foi salva corretamente com hash
        user = User.objects.get(username="john")
        self.assertTrue(user.check_password("secret123"))

class CreateListingTest(APITestCase):
    def setUp(self):
        # Criação de um usuário para o teste
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        
        # Criação de uma categoria para associar à listagem
        self.category = Category.objects.create(categories="Test Category")
        
        # Definir a URL para o endpoint de criação de listagem
        self.url = reverse('api-createListing')
        
        # Autenticar o usuário
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_listing_successful(self):
        # Dados para criar a nova listagem
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": self.category.id  # Associa à categoria criada no setUp
        }
        
        # Realizando o POST para criar a listagem
        response = self.client.post(self.url, data, format='json')
        
        # Verificando se o status é 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificando se a mensagem de sucesso foi retornada
        self.assertEqual(response.data['message'], 'Create Listing Successful.')

        # Verificando se a listagem foi criada no banco de dados
        self.assertEqual(self.category.auctionlisting_set.count(), 1)
        listing = self.category.auctionlisting_set.first()
        self.assertEqual(listing.title, "Test Listing")
        self.assertEqual(listing.description, "This is a test listing")
        self.assertEqual(listing.bidstart, 100)
        self.assertEqual(listing.urlImage, "http://example.com/testimage.jpg")
        self.assertEqual(listing.createdBy, self.user)
    
    def test_create_listing_without_authentication(self):
        # Deslogando o usuário
        self.client.logout()

        # Tentando criar a listagem sem estar autenticado
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": self.category.id
        }
        
        response = self.client.post(self.url, data, format='json')
        
        # Espera-se o status 403 do bloqueio pelo permission_classes = [IsAuthenticated]
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AddCommentTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jane", password="secret123")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(categories="Eletrônicos")
        self.listing = AuctionListing.objects.create(
            title="Notebook Gamer",
            description="RTX 4070, i9, 32GB RAM",
            bidstart=5000,
            urlImage="http://example.com/notebook.jpg",
            category=self.category,
            createdBy=self.user
        )

        self.url = reverse("api-addComment", kwargs={"listing_id": self.listing.id})

    def test_add_comment_successfully(self):
        response = self.client.post(self.url, {"comment": "Produto sensacional!"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Comment send successfully.")

        # Verificar se comentário foi criado no banco
        comment_exists = Comments.objects.filter(
            user=self.user, item=self.listing, comment="Produto sensacional!"
        ).exists()
        self.assertTrue(comment_exists)

    def test_add_comment_without_authentication(self):
        self.client.logout()
        response = self.client.post(self.url, {"comment": "Não deveria funcionar"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_comment_missing_field(self):
        response = self.client.post(self.url, {})  # Sem o campo 'comment'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('comment', response.data)
        self.assertTrue(any('required' in msg.lower() for msg in response.data['comment']))
        self.assertEqual(Comments.objects.count(), 0)