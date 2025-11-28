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
def alt_user(db):
    return User.objects.create_user(
        username="alt_testuser",
        email="alt_teste@teste.com",
        password="123456"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def auction_listing(db, category, user):
    return AuctionListing.objects.create(
        title="Test Auction",
        description="Test Description",
        starting_bid=100,
        image_url="https://pop.proddigital.com.br/wp-content/uploads/sites/8/2021/07/naruto-1.jpg",
        category=category,
        created_by=user
    )

@pytest.fixture
def watchlist_listing(db, alt_user, auction_listing):
    return Watchlist.objects.create(user=alt_user, listing=auction_listing)

@pytest.fixture
def bid(db, alt_user, auction_listing):
    return Bids.objects.create(user=alt_user, amount=150, listing=auction_listing)