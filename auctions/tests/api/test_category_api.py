import pytest
from django.urls import reverse
from rest_framework import status

class TestCategoriesAPI:
    @pytest.fixture(autouse=True)
    def setup(self, db, category):
        self.url = reverse('api-showCategories')
        self.urlAuctions = reverse('api-categoryAuctions', kwargs={'selectedCategory': category.id})
        
    def test_list_categories(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert "categories" in response.data
        
    def test_list_auctions_by_category(self, api_client, auction_listing):
        response = api_client.get(self.urlAuctions)
        assert response.status_code == status.HTTP_200_OK
        assert 'selectedCategory' in response.data
        assert 'categoriesAuctions' in response.data