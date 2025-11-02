import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import Category, User, AuctionListing, Bids

class TestCreateListing:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = reverse('api-createListing')
    
    def test_create_listing_successful(self, authenticated_client, category, user):
        data = {
            "id": 1,
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }
        
        response = authenticated_client.post(self.url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in  response.data
        
        assert AuctionListing.objects.filter(id=1).exists()
        listing = AuctionListing.objects.get(id=1)
        assert listing.title == "Test Listing"
        assert listing.description == "This is a test listing"
        assert listing.bidstart == 100
        assert listing.urlImage == "http://example.com/testimage.jpg"
        assert listing.createdBy == user
    
    def test_create_listing_without_authentication(self, api_client, category):
        api_client.post(reverse('api-logout'))

        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }
        
        response = api_client.post(self.url, data)
        
        # Espera-se o status 403 do bloqueio pelo permission_classes = [IsAuthenticated]
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestIndexView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = reverse('api-auctions')
        
    def test_list_auctions_empty(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_list_auctions_with_data(self, authenticated_client, auction_listing):
        response = authenticated_client.get(self.url)
        assert AuctionListing.objects.filter(id=1).exists()
        assert response.status_code == status.HTTP_200_OK

class TestListingPageView:
    @pytest.fixture(autouse=True)
    def setup(self, auction_listing, db):
        self.url = reverse('api-pageListing', kwargs={'listing_id': auction_listing.id})
        
    def test_get_listing_details(self, authenticated_client, auction_listing):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert 'listing' in response.data
        assert 'bidList' in response.data
        assert 'comments' in response.data
        
    def test_get_nonexistent_listing(self, authenticated_client):
        url = reverse('api-pageListing', kwargs={'listing_id': 9999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCloseAuctionAPI:
    @pytest.fixture(autouse=True)
    def setup(self, db, user, auction_listing):
        self.owner = user
        self.bidder = User.objects.create_user(username="bidder", password="testpass123")
        self.url = reverse('api-closeAuction', kwargs={'listing_id': auction_listing.id})
        
    def test_close_auction(self, authenticated_client, auction_listing):
        Bids.objects.create(bidUser=self.bidder, bid=150, bidItem=auction_listing)
        
        response = authenticated_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar se o leilão foi marcado como fechado
        auction_listing.refresh_from_db()
        assert auction_listing.closed
