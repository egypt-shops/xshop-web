from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import filters, generics


from ..models import Shop
from .serializers import ShopSerializer, ProductSerializer
from xshop.products.models import Product


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
        responses={200: ShopSerializer, 404: "Shop not found"},
    )
    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)

            serializer = self.serializer_class(shop, many=False)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ShopProductListApi(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "barcode"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_product = serializer.save()
        return Response(self.serializer_class(new_product).data)
