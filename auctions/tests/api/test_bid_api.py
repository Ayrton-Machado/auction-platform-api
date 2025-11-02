import pytest
from django.urls import reverse
from rest_framework import status

class TestPlaceBidAPI:
    @pytest.fixture(autouse=True)
    def setup(self, auction_listing):
        self.url = reverse('api-placeBid', kwargs={'listing_id': auction_listing.id})
        
    def test_place_valid_bid(self, authenticated_client):
        response = authenticated_client.post(self.url, {'placebid': 150})
        assert response.status_code == status.HTTP_200_OK
        
    def test_place_invalid_bid(self, authenticated_client):
        response = authenticated_client.post(self.url, {'placebid': 50})  # Menor que bidstart
        assert response.status_code == status.HTTP_400_BAD_REQUEST

