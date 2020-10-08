from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LoginSerializer


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"token": serializer.validated_data.get("token")})
