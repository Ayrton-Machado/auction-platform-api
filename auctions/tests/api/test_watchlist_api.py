import pytest
from django.urls import reverse
from rest_framework import status

class TestWatchlistAPI:
    @pytest.fixture(autouse=True)
    def setup(self, db, auction_listing):
        self.urlListing = reverse('api-watchlistAddAuction', kwargs={'listing_id': auction_listing.id})
        self.urlRemove = reverse('api-watchlistRemove')
        self.url = reverse('api-watchlistAuction')
        
    def test_add_to_watchlist(self, authenticated_client):
        response = authenticated_client.post(self.urlListing)
        assert response.status_code == status.HTTP_200_OK
        
    def test_view_watchlist(self, authenticated_client, watchlist_listing):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_remove_from_watchlist(self, watchlist_listing, authenticated_client):
        response = authenticated_client.post(self.urlRemove, {'removeWatchlist': watchlist_listing.id})
        assert response.status_code == status.HTTP_200_OK
