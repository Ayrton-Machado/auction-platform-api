from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from ..models import User

from django.db import IntegrityError

class AuthService:
    @staticmethod
    @transaction.atomic
    def register_user(username, password, email, confirmation):
        if '@' not in email:
            raise ValidationError("Invalid Email")

        normalized_user = username.lower()
        if User.objects.filter(username__iexact=normalized_user).exists():
            raise ValidationError("Username already exists.")

        normalized_email = email.lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise ValidationError("Email already exists.")

        if password != confirmation:
            raise ValidationError("Passwords must match.")
        # Garante que a senha seja criptografada
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return user