from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auctions.models import User
from auctions.services import UserService
from auctions.serializers.user import DeleteUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError, PermissionDenied

class softDeleteUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)

        serializer = DeleteUserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                UserService.delete_user(
                    user=user,
                    reason=serializer.validated_data["reason"],
                    requesting_user=request.user
                )
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
