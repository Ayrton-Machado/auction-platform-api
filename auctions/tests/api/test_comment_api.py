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
            user=user, item=auction_listing, comment="Produto sensacional!"
        ).exists()

    def test_add_comment_without_authentication(self, api_client):
        response = api_client.post(self.url, {"comment": "AIAIAI UIUIUI"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_comment_missing_field(self, authenticated_client):
        response = authenticated_client.post(self.url, {})  # Sem o campo 'comment'
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "comment" in response.data 
        assert Comments.objects.count() == 0
