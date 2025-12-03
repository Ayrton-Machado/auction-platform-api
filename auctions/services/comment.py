from django.db import transaction
from django.utils import timezone
from ..models import Comments
from django.core.exceptions import ValidationError

class CommentService:
    @staticmethod
    @transaction.atomic
    def send_comment(user, listing, comment):
        if listing.closed:
            raise ValidationError("Cannot comment on a closed auction.")

        comment_obj = Comments.objects.create(
            user=user,
            listing=listing,
            comment=comment
        )

        return comment_obj