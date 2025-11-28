import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import Comments

class TestAddComment:
    @pytest.fixture(autouse=True)
    def setup(self, db, auction_listing):
        self.url = reverse("api-addComment", kwargs={"listing_id": auction_listing.id})

    def test_add_comment_successfully(self, authenticated_client, user, auction_listing):
        response = authenticated_client.post(self.url, {"comment": "Produto sensacional!"})
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in response.data
        #Verificar se comentário foi criado no Banco
        assert Comments.objects.filter(
            user=user, listing=auction_listing, comment="Produto sensacional!"
        ).exists()

    def test_add_comment_without_authentication(self, api_client):
        response = api_client.post(self.url, {"comment": "AIAIAI UIUIUI"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_comment_missing_field(self, authenticated_client):
        response = authenticated_client.post(self.url, {})  # Sem o campo 'comment'
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "comment" in response.data 
        assert Comments.objects.count() == 0

    def test_add_comment_to_nonexistent_auction(self, authenticated_client):
        """Testa comentar em auction que não existe"""
        url = reverse("api-addComment", kwargs={"listing_id": 9999})
        response = authenticated_client.post(url, {"comment": "Test"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_add_comment_to_closed_auction(self, authenticated_client, auction_listing):
        """Testa se pode comentar em auction fechado"""
        auction_listing.closed = True
        auction_listing.save()
        
        response = authenticated_client.post(self.url, {"comment": "Late comment"})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    
    def test_add_empty_comment(self, authenticated_client):
        """Testa comentário vazio"""
        response = authenticated_client.post(self.url, {"comment": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_add_comment_max_length(self, authenticated_client):
        """Testa comentário muito longo"""
        long_comment = "a" * 250
        response = authenticated_client.post(self.url, {"comment": long_comment})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
