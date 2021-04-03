from drf_yasg2.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout

from .serializers import TokenApiSerializer, TokenResponseSerializer


class TokenApi(APIView):
    """Get user's token and basic data"""

    serializer_class = TokenApiSerializer

    @swagger_auto_schema(
        operation_description="Generate new token for user",
        request_body=TokenApiSerializer,
        responses={
            200: TokenResponseSerializer,
            400: "Invalid mobile number/password or both",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        vd = serializer.validated_data
        resp_data = {
            "token": vd.get("token"),
            "user": {
                "name": vd.get("name"),
                "mobile": vd.get("mobile"),
                "email": vd.get("email"),
                "type": vd.get("type"),
            },
        }

        resp_serializer = TokenResponseSerializer(data=resp_data)
        resp_serializer.is_valid()
        return Response(resp_serializer.data)


class Logout(LoginRequiredMixin, APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            auth_logout(request.user)
            logout(request)
        return Response(status=status.HTTP_200_OK)
