from rest_framework import serializers
from .models import AuctionListing

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = '__all__'  # Ou liste campos específicos: ['id', 'title', ...]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()