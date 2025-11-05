from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..models import Category, AuctionListing
from ..serializers import CategorySerializer, AuctionSerializer

@extend_schema(
    summary="Buscar Todas Categorias",
    responses={
        200: {'description': "Sucesso ao Buscar"},
        400: {'description': "Erro ao Buscar Categorias"}
    },
    tags=['Categories']
)
class ShowCategoriesAPI(APIView):   
    def get(self, request):
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True).data
        return Response({
            "categories" : categories_serializer
        }, status=status.HTTP_200_OK)
