from rest_framework import serializers
from ..models import Bids

class PlaceBidSerializer(serializers.Serializer):
    placebid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        error_messages={
            'required': 'Bid amount is required.',
            'invalid': 'Please enter a valid number.',
            'min_value': 'Bid must be greater than zero.'
        }
    )

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = '__all__'
