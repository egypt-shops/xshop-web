from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema

from ..models import Shop
from .serializers import ShopSerializer


class ShopListApi(APIView):
    serializer_class = ShopSerializer

    @swagger_auto_schema(
        operation_description="List all shops that exists in the DB",
        responses={200: "[List of shops]"},
    )
    def get(self, request):
        shops = Shop.objects.all()

        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data)


class ShopDetailApi(APIView):
    serializer_class = ShopSerializer

    @swagger_auto_schema(
        operation_description="Get specific shop's data",
        responses={200: ShopSerializer, 400: "Shop not found"},
    )
    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)

            serializer = self.serializer_class(shop, many=False)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
