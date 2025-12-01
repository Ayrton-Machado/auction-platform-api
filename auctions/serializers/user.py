from rest_framework import serializers
from ..models import User

class DeleteUserSerializer(serializers.Serializer):
    reason = serializers.CharField(
        min_length=10,
        allow_blank=False,
        required=True
    )

    confirm = serializers.BooleanField(required=True)

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError("You must confirm the deletion.")
        return value
