from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework import generics


class LoginAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"token": serializer.validated_data.get("token")})
