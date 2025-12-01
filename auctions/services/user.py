from django.db import transaction
from django.utils import timezone
from ..models import User

class UserService:
    @staticmethod
    @transaction.atomic
    def delete_user(user, reason, requesting_user):
        if user != requesting_user:
            raise PermissionError("You can delete only your account.")

        if user.deleted_at is not None or user.is_active is False:  # Só define se ainda não foi deletado
            raise ValueError("This account has already been deleted.")

        user.deleted_at = timezone.now()
        user.is_active = False  # Impede login
        user.deletion_reason = reason
        user.save()
        return user.deleted_at
        