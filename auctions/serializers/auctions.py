from rest_framework import serializers
from ..models import Category, AuctionListing

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = '__all__'  # Ou liste campos específicos: ['id', 'title', ...]


class CreateListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionListing
        fields = ["title", "description", "bidstart", "urlImage", "category"]
    
    def create(self, validated_data):
        if 'category' not in validated_data or validated_data['category'] is None:
            validated_data['category'] = Category.objects.get(categories="Outro")
        validated_data['createdBy'] = self.context['request'].user
        return AuctionListing.objects.create(**validated_data)