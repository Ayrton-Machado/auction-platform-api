from rest_framework import serializers
from ..models import Watchlist

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'

class WatchlistAddAuctionSerializer(serializers.Serializer):
    class Meta:
        model = Watchlist
        fields = ["user", "item"]
    
    def create(self, validated_data):
        validated_data['createdBy'] = self.context['request'].user
