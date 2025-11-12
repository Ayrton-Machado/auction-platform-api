import pytest
from django.urls import reverse
from rest_framework import status
from auctions.models import User, Bids

class TestPlaceBidAPI: #Zombies
    @pytest.fixture(autouse=True)
    def setup(self, db, auction_listing):
        self.bidder = User.objects.create_user(
            username="Test_Bidder",
            email="bidder@teste.com",
            password="12345"
        )
        self.url = reverse('api-placeBid', kwargs={'listing_id': auction_listing.id})

    # Zero Cases
    def test_place_bid_without_auth(self, api_client):
        response = api_client.post(self.url, {'placebid': 150})
        assert response.status_code == status.HTTP_403_FORBIDDEN # Erro 403 para erro de permissao

    def test_place_bid_null_value(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {'placebid': None})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_bid_missing_field(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # One Cases
    def test_place_valid_bid(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {'placebid': 150.90})
        assert response.status_code == status.HTTP_200_OK

    def test_place_bid_increases_own_bid(self, api_client, auction_listing):
        api_client.force_authenticate(user=self.bidder)
        api_client.post(self.url, {'placebid': 150})
        response = api_client.post(self.url, {'placebid': 160})

        assert response.status_code == status.HTTP_400_BAD_REQUEST # Usuário não pode sobrepujar sua própria bid

        highest_bid = Bids.objects.filter(bidItem=auction_listing).order_by('-bid').first()
        assert highest_bid.bid == 150 # Verificar bid no Banco
        assert highest_bid.bidUser == self.bidder # Verificar user no banco  

    def test_place_bid_increases_another_bid(self, db, api_client, auction_listing):
        api_client.force_authenticate(user=self.bidder)
        api_client.post(self.url, {'placebid': 150}) # Enviar primeira Bid

        api_client.post(reverse('api-logout')) 

        another_bidder = User.objects.create_user(
            username="test_another_bidder",
            email="anotherbidder@teste.com",
            password="12345"
        )

        api_client.force_authenticate(user=another_bidder)
        response = api_client.post(self.url, {'placebid': 160.2}) # Enviar outra bid
        assert response.status_code == status.HTTP_200_OK

        highest_bid = Bids.objects.filter(bidItem=auction_listing).order_by('-bid').first()

        assert highest_bid.bid == 160.2 # Verifica se bid foi atualizada corretamente
        assert highest_bid.bidUser == another_bidder # Verifica se user é atualizado

        # Verificar bids no Banco
        total_bids = Bids.objects.filter(bidItem=auction_listing).count()
        assert total_bids == 2

    # Many Cases // Tornar Simples
    @pytest.mark.skip(reason="Implementar Futuramente")
    def test_place_many_bids_multiple_users(self): pass

    @pytest.mark.skip(reason="Implementar Futuramente")
    def test_place_many_bids_sequential(self): pass

    # Boundary
    def test_place_bid_lower_than_current_highest(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        api_client.post(self.url, {'placebid': 150}) # Enviar primeira Bid

        api_client.post(reverse('api-logout')) 

        another_bidder = User.objects.create_user(
            username="test_another_bidder",
            email="anotherbidder@teste.com",
            password="12345"
        )

        api_client.force_authenticate(user=another_bidder)
        response = api_client.post(self.url, {'placebid': 148}) # Enviar outra bid menor
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_bid_zero_value(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {'placebid': 0}) # Enviar bid 0
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Bid deve ser maior que 0

    def test_place_bid_on_closed_auction(self, api_client, authenticated_client, auction_listing):
        api_client.force_authenticate(user=self.bidder)

        url = reverse('api-closeAuction', kwargs={'listing_id': auction_listing.id})
        authenticated_client.post(url) # Fecha Leilao

        auction_listing.refresh_from_db() # Verificar no Banco
        assert auction_listing.closed is True
        response = api_client.post(self.url, {'placebid': 150}) # Enviar bid com leilao fechado
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_bid_invalid_type_string(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {'placebid': "15O"}) # Enviar string ao inves de Decimal
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_bid_as_owner(self, authenticated_client):
        response = authenticated_client.post(self.url, {"placebid": 180.40})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_place_bid_less_than_bidstart(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.post(self.url, {'placebid': 50})  # Menor que bidstart

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_negative_bid(self, api_client):
        api_client.force_authenticate(user=self.bidder)

        response = api_client.post(self.url, {'placebid': -50})  # Menor que zero
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_place_bid_nonexist_listing(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        url = reverse('api-placeBid', kwargs={'listing_id': 9999}) # Nonexist ID
        response = api_client.post(url, {'placebid': 150})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_place_bid_invalid_url(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        url = '/api/listing/abc/bid' # Nonexist ID
        response = api_client.post(url, {'placebid': 150})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # Interface
    @pytest.mark.skip(reason="Implementar Futuramente")
    def test_place_bid_response_structure(self): pass

    def test_place_bid_wrong_method(self, api_client):
        api_client.force_authenticate(user=self.bidder)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

