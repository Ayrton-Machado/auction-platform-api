from rest_framework import serializers
from ..models import Bids

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = '__all__'
