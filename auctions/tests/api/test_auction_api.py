import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import Category, User, AuctionListing, Bids

class TestCreateListing: # Zombies
    @pytest.fixture(autouse=True)
    def setup(self, category):
        self.url = reverse('api-createListing')
        self.data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }

    # Zero Cases
    def test_create_listing_empty_data(self, authenticated_client):
        data = {}
        
        response = authenticated_client.post(self.url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Verificar status de retorno

        assert AuctionListing.objects.count() == 0 # Verificar que não foi criado no banco

    def test_create_listing_without_auth(self, api_client):

        response = api_client.post(self.url, self.data) # Enviar input sem auth

        assert response.status_code == status.HTTP_403_FORBIDDEN # Verificar status

        assert AuctionListing.objects.count() == 0  # Verificar que não foi criado no banco

    # One Cases
    def test_create_listing_successful(self, authenticated_client, category, user):
        response = authenticated_client.post(self.url, self.data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        assert AuctionListing.objects.filter(title="Test Listing").exists()
        listing = AuctionListing.objects.get(title="Test Listing")
        assert listing.title == "Test Listing"
        assert listing.description == "This is a test listing"
        assert listing.bidstart == 100
        assert listing.urlImage == "http://example.com/testimage.jpg"
        assert listing.createdBy == user
        assert listing.category == category

    # Boundary
    def test_create_listing_invalid_input(self, authenticated_client):
        data = {
            "title": 5, # expects string
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": "10" # expects object
        }

        response = authenticated_client.post(self.url, data) # tenta enviar
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Verifica retorno
        # Verifica especificidade do erro
        assert "title" in response.data
        assert "category" in response.data 

    def test_create_listing_nonexist_category(self, authenticated_client):
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 100,
            "urlImage": "http://example.com/testimage.jpg",
            "category": 9999 # doesn't exist
        }

        response = authenticated_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_listing_negative_bidstart(self, authenticated_client, category):
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": -10,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }

        response = authenticated_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_listing_zero_bidstart(self, authenticated_client, category):
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": 0,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }

        response = authenticated_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_nonexist_bidstart(self, authenticated_client, category):
        data = {
            "title": "Test Listing",
            "description": "This is a test listing",
            "bidstart": None,
            "urlImage": "http://example.com/testimage.jpg",
            "category": category.id
        }

        response = authenticated_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Interface
    def test_create_listing_wrong_method(self, authenticated_client):
        response = authenticated_client.get(self.url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

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


class TestCloseAuctionAPI: # Zombies
    @pytest.fixture(autouse=True)
    def setup(self, db, user, auction_listing):
        self.owner = user
        self.bidder = User.objects.create_user(username="bidder", password="testpass123")
        self.bid = Bids.objects.create(bidUser=self.bidder, bid=180, bidItem=auction_listing)
        self.url = reverse('api-closeAuction', kwargs={'listing_id': auction_listing.id})
        self.urlAuction = reverse('api-pageListing', kwargs={'listing_id': auction_listing.id})

    # Zero Cases
    def test_close_auction_nonexistent_listing(self, authenticated_client):
        url = reverse('api-closeAuction', kwargs={'listing_id': 5})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_close_auction_without_auth(self, api_client):
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_close_auction_without_bid(self, authenticated_client, user, category, auction_listing):
        auction = AuctionListing.objects.create(
            title="Test Auction",
            description="Test Description",
            bidstart=100,
            category=category,
            createdBy=user
        )
        url = reverse('api-closeAuction', kwargs={'listing_id': auction.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar se o leilão foi marcado como fechado
        auction.refresh_from_db()
        assert auction.closed

    # One Cases
    def test_close_auction_one_bid(self, authenticated_client, auction_listing):
        response = authenticated_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar se o leilão foi marcado como fechado
        auction_listing.refresh_from_db()
        assert auction_listing.closed
    
    def test_close_auction_one_bid_owner_not_winner(self, authenticated_client):

        responseOwner = authenticated_client.post(self.url) # Fecha listing como owner
        
        assert responseOwner.status_code == status.HTTP_200_OK # Verifica se fechou corretamente 
        
        assert responseOwner.data['winner'] == False # Garante que o owner não é o vencedor, pois houve a bid maior que a bidstart
    
    # Boundary
    def test_close_auction_not_owner(self, api_client, auction_listing):
        # criar novo user
        another_user = User.objects.create_user(
            username="another_user",
            email="anotheruser@teste.com",
            password="12345"
        )
        
        api_client.force_authenticate(user=another_user) # logar novo user
        
        responseAnotherUser = api_client.post(self.url) # tenta fechar auction
        
        assert responseAnotherUser.status_code == status.HTTP_403_FORBIDDEN # verificar retorno correto

        auction_listing.refresh_from_db()
        assert auction_listing.closed is False # verifica se leilao nao foi fechado no banco

    def test_close_auction_already_closed(self, authenticated_client, auction_listing):
        
        responseOwner = authenticated_client.post(self.url) # Fecha listing como owner
        
        assert responseOwner.status_code == status.HTTP_200_OK # Verifica se fechou corretamente 
        
        responseCloseAgain = authenticated_client.post(self.url) # Tentar Fechar novamente
        
        assert responseCloseAgain.status_code == status.HTTP_400_BAD_REQUEST # Verificar status de retorno

        #Verificar se está fechado no banco
        auction_listing.refresh_from_db()
        assert auction_listing.closed is True

    def test_close_auction_with_invalid_listing_id_format(self, authenticated_client):
        url = '/api/listing/abc/close'
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

