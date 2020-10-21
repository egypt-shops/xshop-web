from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Product
from .serializers import ProductSerializer


class ProductListCreateApi(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_product = serializer.save()
        return Response(self.serializer_class(new_product).data)


class ProductDetailPatchApi(APIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            serializer = self.serializer_class(product, many=False)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_product = serializer.save()
            return Response(self.serializer_class(updated_product).data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
