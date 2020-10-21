from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..models import Shop
from .serializers import ShopSerializer


class ShopListApi(APIView):
    serializer_class = ShopSerializer

    def get(self, request):
        shops = Shop.objects.all()

        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data)


class ShopDetailApi(APIView):
    serializer_class = ShopSerializer

    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)

            serializer = self.serializer_class(shop, many=False)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
