from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenApiSerializer


class TokenApi(APIView):
    """Get user's token and basic data"""

    serializer_class = TokenApiSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        vd = serializer.validated_data
        return Response(
            {
                "token": vd.get("token"),
                "user": {
                    "name": vd.get("name"),
                    "mobile": vd.get("mobile"),
                    "email": vd.get("email"),
                    "type": vd.get("type"),
                },
            }
        )
