from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

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
        data = serializer.validated_data
        product = Product.objects.create(
            **data, added_by=request.user, shop=request.user.shop
        )
        return Response(self.serializer_class(product).data)


class ProductDetailPatchApi(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        description="Get product's info",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Patch existing product in specific shop",
        request=ProductSerializer,
        responses={404: "Product not found"},
    )
    def patch(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if not user.is_superuser and (
            product.added_by != user or product.shop != user.shop
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_product = serializer.save()
        return Response(self.serializer_class(updated_product).data)


class ListProductsPerShop(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        description="List products per shop",
        responses={200: ProductSerializer, 404: "Shop not found"},
    )
    def get(self, request, shop_subdomain):
        shop = get_object_or_404(Shop, subdomain=shop_subdomain)
        products = Product.objects.filter(shop=shop)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)
