import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from auctions.models import *

User = get_user_model()

@pytest.fixture
def api_client():
    """
    Cliente API não autenticado.
    - Formato JSON por padrão (elimina format='json' nos testes)
    - Usar para endpoints públicos ou testes de autenticação
    """
    client = APIClient()
    client.default_format = 'json'
    return client

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="teste@teste.com",
        password="12345"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(categories="Test Category")

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def auction_listing(db, category, user):
    return AuctionListing.objects.create(
        id=1,
        title="Test Auction",
        description="Test Description",
        bidstart=100,
        category=category,
        createdBy=user
    )

@pytest.fixture
def watchlist_listing(db, user, auction_listing):
    return Watchlist.objects.create(user=user, item=auction_listing)

@pytest.fixture
def bid(db, user, auction_listing):
    return Bids.objects.create(bidUser=user, bid=150, bidItem=auction_listing)