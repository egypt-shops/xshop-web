from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Product
from .serializers import ProductSerializer
from xshop.shops.models import Shop


class ProductListCreateApi(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_set = Product.objects.prefetch_related("shop").all()
        shop_id = self.request.query_params.get("shop_id", None)

        if shop_id is not None:
            query_set = query_set.filter(shop=shop_id)
        return query_set

    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "barcode"]

    @extend_schema(
        description="Create new product in specific shop",
        request=ProductSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_product = serializer.save()
        return Response(self.serializer_class(new_product).data)


class ProductDetailPatchApi(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        description="Get product's info",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            serializer = self.serializer_class(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Patch existing product in specific shop",
        request=ProductSerializer,
        responses={404: "Product not found"},
    )
    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_product = serializer.save()
            return Response(self.serializer_class(updated_product).data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ListProductsPerShop(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        description="List products per shop",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def get(self, request, shop_id):
        try:
            Shop.objects.get(id=shop_id)
            products = Product.objects.filter(shop_id=shop_id)

            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
