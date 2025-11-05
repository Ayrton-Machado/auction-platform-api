from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from drf_spectacular.utils import extend_schema

from ..models import AuctionListing
from ..serializers import AddCommentSerializer

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
        item = get_object_or_404(AuctionListing, id=listing_id)

        serializer = AddCommentSerializer(
            data=request.data,
            context={'request': request, "item": item}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment send successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
