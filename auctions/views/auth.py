from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from django.db import IntegrityError
from ..serializers import LoginSerializer, RegisterSerializer

@extend_schema(
    summary="Loga-te",
    request=LoginSerializer,
    responses={
        200: {'description': "Login bem-sucedido"},
        400: {'description': "Dados inválidos"}
    },
    tags=['Authentication']
)
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Attempt to sign user in
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return Response({
                    "message": "Login Successful.",
                    "user": {
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Invalid username and/or password."
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Registra-te",
    request=RegisterSerializer,
    responses={
        200: {'description': "Registro bem-sucedido"},
        400: {'description': "Dados inválidos"}
    },
    tags=['Authentication']
)
class RegisterAPI(APIView):      
    def post(self, request):
        confirmation = request.data.get("confirmation")

        if request.data.get("password") != confirmation:
            return Response({
                "error": "Passwords must match."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                login(request, user)

                return Response({
                    "message": "Register Successful.",
                    "user": {
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({
                    "message": "Username already taken."
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Logout-ta-te",
    responses={
        200: {'description': "Logout Bem-Sucedido."},
        400: {'description': "Erro ao sair."}
    },
    tags=['Authentication']
)
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({
                "message": "Log Out Successful"
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "User is not logged"
        }, status=status.HTTP_400_BAD_REQUEST)