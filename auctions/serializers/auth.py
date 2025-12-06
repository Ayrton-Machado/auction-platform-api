from rest_framework import serializers
from ..models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmation"]
        extra_kwargs = {
            "username": {"min_length": 3},
            "password": {"write_only": True}
        }