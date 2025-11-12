from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..services import BidService

# Banco de dados
from ..models import AuctionListing, Bids
from ..serializers import BidSerializer, PlaceBidSerializer

@extend_schema(
    summary="Enviar Bid",
    request=BidSerializer,
    responses={
        200: {'description': "Bid Enviada Com Sucesso."},
        400: {'description': "Erro ao Enviar Bid"}
    },
    tags=['Bid']
)
class PlaceBidAPI(APIView):
    permission_classes = [IsAuthenticated]        

    def post(self, request, listing_id):
        # Instanceia de serializer para validação
        serializer = PlaceBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Valida dados
        listingItem = get_object_or_404(AuctionListing, id=listing_id)
        print(serializer._errors)

        try:
            place_bid = BidService.place_bid(
                listingData=listingItem, 
                user=request.user, 
                amount=serializer.validated_data["placebid"]
            )

            listingItem.refresh_from_db()

            return Response({
                "message": "Bid placed successfully.",
                "bid": str(place_bid.bid),
                "current_highest": str(listingItem.bidstart)
            }, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
            

