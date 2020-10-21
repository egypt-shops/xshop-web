from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Shop
from .serializers import ShopSerializer


class ShopListApi(APIView):
    serializer_class = ShopSerializer

    def get(self, request):
        shops = Shop.objects.all()

        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data)
