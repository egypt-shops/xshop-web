from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi

from ..models import Product
from .serializers import ProductSerializer

# query parameter used to filter shops by id to return list per shop
shop_id = openapi.Parameter(
    "shop_id",
    openapi.IN_QUERY,
    description="Shop's identification number",
    type=openapi.TYPE_INTEGER,
)


class ProductListCreateApi(APIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_set = Product.objects.prefetch_related("shop").all()
        shop_id = self.request.query_params.get("shop_id", None)

        if shop_id is not None:
            query_set = query_set.filter(shop=shop_id)
        return query_set

    @swagger_auto_schema(
        operation_description="List all products in specific shop",
        manual_parameters=[shop_id],
        responses={200: "List of products"},
    )
    def get(self, request):
        products = self.get_queryset()

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create new product in specific shop",
        request_body=ProductSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_product = serializer.save()
        return Response(self.serializer_class(new_product).data)


class ProductDetailPatchApi(APIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="List product's info",
        responses={200: ProductSerializer, 400: "Product not found"},
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            serializer = self.serializer_class(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Patch existing product in specific shop",
        request_body=ProductSerializer,
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
