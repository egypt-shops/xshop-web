from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout

from .serializers import (
    TokenApiSerializer,
    TokenResponseSerializer,
    RegistrationSerializer,
)


class TokenApi(APIView):
    """Get user's token and basic data"""

    serializer_class = TokenApiSerializer

    @extend_schema(
        description="Generate new token for user",
        request=TokenApiSerializer,
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
        request.user.auth_token.delete()
        auth_logout(request)
        return Response(status=status.HTTP_200_OK)


class Registration(APIView):
    @extend_schema(
        description="Generate new user",
        request=RegistrationSerializer,
        responses={
            200: '{"name": "user name", "mobile": "user mobile"}',
            400: "Invalid mobile number/password or both",
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if not serializer.is_valid():
            return Response(
                {"message": "failure", "error": serializer.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        data["response"] = "successfully registered a new user"
        data["name"] = user.name
        data["mobile"] = str(user.mobile)
        return Response(data, status=status.HTTP_200_OK)
