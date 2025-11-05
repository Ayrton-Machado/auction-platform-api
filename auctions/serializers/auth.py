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
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        # Garante que a senha seja criptografada
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
