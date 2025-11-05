from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from ..models import AuctionListing, Comments, Bids, Category
from ..serializers import CategorySerializer, CreateListingSerializer, CommentsSerializer, BidSerializer, AuctionSerializer

@extend_schema(
    summary="Buscar todas auctions",
    responses={
        200: {'description': "Sucesso na busca."},
        400: {'description': "Erro ao buscar."}
    },
    tags=['Auctions']
)
class indexAPI(APIView):
    def get(self, request):
        auctions = AuctionListing.objects.all()
        if not auctions.exists():
            return Response({"message": "No auctions available."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'auctions': list(auctions.values())})

@extend_schema(
    summary="Criar Auction",
    request=CreateListingSerializer,
    responses={
        200: {'description': "Auction criada com sucesso"},
        400: {'description': "Erro ao criar listing."}
    },
    tags=['Auctions']
)
class CreateListingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateListingSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    "message": "Create Listing Successful.",
                    "listing": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error saving to the database."})
        return Response({
            "message": "Invalid data. Please correct the errors and try again.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Buscar dados completos de uma auction",
    responses={
        200: {'description': "Listing Encontrada."},
        404: {'description': "Listing Não Encontrada."},
        400: {'description': "Erro ao buscar listing."}
    },
    tags=['Auctions']
)
class ListingPageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, listing_id):
        try:
            listingItem = AuctionListing.objects.get(id=listing_id)
        except AuctionListing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

        allComments = Comments.objects.filter(item=listingItem)
        bidsItem = Bids.objects.filter(bidItem=listingItem)
        lastBid = bidsItem.last()
        isOwner = request.user == listingItem.createdBy

        # Apenas define "win" se o leilão estiver fechado e houver um último lance
        win = False
        if listingItem.closed and lastBid is not None:
            win = request.user == lastBid.bidUser


        #data
        allCommentsData = CommentsSerializer(allComments, many=True).data
        bidsItemData = BidSerializer(bidsItem, many=True).data
        listingItemData = AuctionSerializer(listingItem).data
        bidAmount = bidsItem.count()


        return Response({
            'listing': listingItemData,
            'bidList': bidsItemData,
            'bidAmount': bidAmount,
            'win': win,
            'isOwner': isOwner,
            'comments': allCommentsData
        }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Buscar Listagens em uma categoria",
    responses={
        200: {'description': "Sucesso ao Buscar auctions"},
        400: {'description': "Erro ao Buscar auctions"}
    },
    tags=['Categories']
)
class CategoriesAuctionsAPI(APIView):
    def get(self, request, selectedCategory):
        category = Category.objects.filter(id = selectedCategory).first()
        categoriesAuctions = AuctionListing.objects.filter(category=category)

        if category is None or not categoriesAuctions.exists():
            return Response({"message": "Category or Auctions in this Category does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        categorySerializer = AuctionSerializer(categoriesAuctions, many=True).data
        nameCategorySerializer = CategorySerializer(category).data

        return Response({
            'selectedCategory': nameCategorySerializer,
            'categoriesAuctions': categorySerializer,
        }, status=status.HTTP_200_OK)

@extend_schema(
    summary="Fechar Auction",
    responses={
        200: {'description': "Listing Fechada."},
        404: {'description': "Listing Não Encontrada."},
        400: {'description': "Erro ao buscar listing."}
    },
    tags=['Auctions']
)
class CloseAuctionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, listing_id):
        listingItem = AuctionListing.objects.get(id=listing_id)
        lastBid = Bids.objects.filter(bidItem=listingItem).last()
        listingItem.closed = True
        listingItem.save()
        close = listingItem.closed
        if close == True:
            if close == True and request.user == lastBid.bidUser:
                winner = True
            elif close == True and request.user != lastBid.bidUser:
                winner = False
            return Response({
                "winner": winner
            })
        else:
            return Response({"message": "Auction closed successfully."}, status=status.HTTP_200_OK)
