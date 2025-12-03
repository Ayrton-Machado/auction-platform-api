from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ValidationError, PermissionDenied
from ..models import AuctionListing, Comments, Bids, Category
from ..serializers import CategorySerializer, CreateListingSerializer, CommentsSerializer, BidSerializer, AuctionSerializer
from ..services import AuctionService

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
            return Response({"message": "No auctions available."}, status=status.HTTP_200_OK)
        return Response({'auctions': list(auctions.values())})

@extend_schema(
    summary="Criar Auction",
    request=CreateListingSerializer,
    responses={
        201: {'description': "Create Listing Successful."},
        400: {'description': "Erro ao criar listing."}
    },
    tags=['Auctions']
)
class CreateListingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        listing_serializer = CreateListingSerializer(data=request.data, context={"request": request})

        if listing_serializer.is_valid():
            try:
                AuctionService.create_listing(
                    listing_data = listing_serializer,
                    user=request.user
                )

                return Response({
                    "message": "Create Listing Successful."
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": "Error saving to the database."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "Invalid data. Please correct the errors and try again.",
            "errors": listing_serializer.errors
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

        allComments = Comments.objects.filter(listing=listingItem)
        bidsItem = Bids.objects.filter(listing=listingItem)
        lastBid = bidsItem.last()
        isOwner = request.user == listingItem.created_by

        # Apenas define "win" se o leilão estiver fechado e houver um último lance
        win = False
        if listingItem.closed and lastBid is not None:
            win = request.user == lastBid.user

        #data
        allCommentsData = CommentsSerializer(allComments, many=True).data
        bidsItemData = BidSerializer(bidsItem, many=True).data
        listingItemData = AuctionSerializer(listingItem).data
        bidAmount = bidsItem.count()


        return Response({
            'listing': listingItemData,
            'bids': bidsItemData,
            'amount': bidAmount,
            'win': win,
            'is_owner': isOwner,
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
        category = Category.objects.filter(id=selectedCategory).first()
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
        listing = get_object_or_404(AuctionListing, id=listing_id)
        last_bid = Bids.objects.filter(listing=listing).last()

        last_bid_amount = last_bid.amount if last_bid else None
        last_bid_user = last_bid.user if last_bid else None

        try: 
            close_auction = AuctionService.close_auction(
                listing=listing,
                last_bid_user=last_bid_user,
                last_bid_amount=last_bid_amount,
                requesting_user=request.user
            )

            return Response({
                "message": "Auction closed successfully."
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except PermissionDenied as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )