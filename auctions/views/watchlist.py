from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..models import AuctionListing, Watchlist
from ..serializers import WatchlistSerializer

@extend_schema(
    summary="Adicionar listing à watchlist",
    request=WatchlistSerializer,
    responses={
        200: {'description': "Registro bem-sucedido"},
        400: {'description': "Dados inválidos"}
    },
    tags=['Wathclist']
)
class WatchlistAddAuctionAPI(APIView):
    def post(self, request, listing_id):
        user = request.user
        item = AuctionListing.objects.get(id=listing_id)
        watchlist = Watchlist(user=user, listing=item)
        watchlist.save()

        return Response({
            'message': 'Successfully added to watchlist'
        }, status=status.HTTP_200_OK)

@extend_schema(
    summary="Busca de auctions na WatchList",
    request=WatchlistSerializer,
    responses={
        200: {'description': "Sucesso ao buscar listings"},
        404: {'description': "Lista vazia."},
        400: {'description': "Erro ao buscar."}
    },
    tags=['Wathclist']
)
class WatchlistAuctionAPI(APIView):
    def get(self, request):
        user = request.user.id
        userWatchlist = Watchlist.objects.filter(user=user)
        if not userWatchlist.exists():
            return Response({"message": "Watchlist is empty."}, status=status.HTTP_404_NOT_FOUND)
        userWatchlistData = WatchlistSerializer(userWatchlist, many=True).data

        return Response({
            'watchlist': userWatchlistData
        }, status=status.HTTP_200_OK)

@extend_schema(
    summary="Remover auction da WatchList",
    request=WatchlistSerializer,
    responses={
        200: {'description': "Sucesso ao deletar listing"},
        400: {'description': "Erro ao remover."}
    },
    tags=['Wathclist']
)
class WatchlistRemoveAPI(APIView):
    def post(self, request):
        listing_id = request.data.get('removeWatchlist')
        item = Watchlist.objects.get(id=listing_id)
        item.delete()
        return Response({"message": "Auction successfully removed from watchlist."}, status=status.HTTP_200_OK)
