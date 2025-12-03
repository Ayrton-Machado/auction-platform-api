from rest_framework import serializers
from ..models import Category, AuctionListing
from decimal import Decimal

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = '__all__'  # Ou liste campos específicos: ['id', 'title', ...]


class CreateListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "image_url", "category"]