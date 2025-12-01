from rest_framework import serializers
from ..models import Bids

class PlaceBidSerializer(serializers.Serializer):
    placebid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
    )

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = '__all__'
