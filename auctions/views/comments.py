from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ValidationError
from ..models import AuctionListing
from ..serializers import AddCommentSerializer
from ..services import CommentService

@extend_schema(
    summary="Enviar comentário",
    request=AddCommentSerializer,
    responses={
        200: {'description': "Comentário enviado"},
        400: {'description': "Erro ao enviar comentário, tente novamente."}
    },
    tags=['Comments']
)
class AddCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, listing_id):
        listing = get_object_or_404(AuctionListing, id=listing_id)

        serializer = AddCommentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            try:
                CommentService.send_comment(
                    user=request.user,
                    listing=listing,
                    comment=serializer.validated_data["comment"]
                )

                return Response({"message": "Comment send successfully."}, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)