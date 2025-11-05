from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

# Banco de dados
from ..models import AuctionListing, Bids
from ..serializers import BidSerializer

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
        listingItem = AuctionListing.objects.get(id=listing_id)
        bidstart = listingItem.bidstart
        bid = int(request.data.get('placebid'))
        bidUser = request.user
        if bid > bidstart:
            listingItem.bidstart = bid
            Bids(bidUser=bidUser, bid=bid, bidItem=listingItem).save()
            listingItem.save()
            return Response({"message": "Bid placed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Bid must be higher than current bid.",
                "current_bid": bidstart
            }, status=status.HTTP_400_BAD_REQUEST)

