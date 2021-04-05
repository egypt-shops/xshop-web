from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Shop
from .serializers import ShopSerializer


class ShopListApi(APIView):
    serializer_class = ShopSerializer

    @extend_schema(
        description="List all shops that exists in the DB",
        responses={200: "[List of shops]"},
    )
    def get(self, request):
        shops = Shop.objects.all()

        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data)


class ShopDetailApi(APIView):
    serializer_class = ShopSerializer

    @extend_schema(
        description="Get specific shop's data",
        responses={200: ShopSerializer, 404: "Shop not found"},
    )
    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)

            serializer = self.serializer_class(shop, many=False)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
