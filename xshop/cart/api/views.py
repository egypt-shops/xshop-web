from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg2.utils import swagger_auto_schema


from xshop.products.models import Product
from .serializers import AddToCartSerializer
from ..cart import Cart


class AddToCartApi(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add product to cart",
        request_body=AddToCartSerializer,
        responses={
            200: AddToCartSerializer,
            400: "product_id Not found or Invalid quantity",
        },
    )
    def post(self, request):
        cart = Cart(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data.get("product")

        cart.add(
            product=product,
            quantity=serializer.validated_data.get("quantity"),
            override_quantity=serializer.validated_data.get("override_quantity"),
        )
        return Response(cart)

    @swagger_auto_schema(
        operation_description="get cart's product",
        responses={
            200: AddToCartSerializer,
            404: "Cart's product not found",
        },
    )
    def get(self, request):
        cart = Cart(request)

        return Response(cart)

    @swagger_auto_schema(
        operation_description="delete cart from session",
        responses={
            200: "Cart removed from session",
            404: "Cart not found",
        },
    )
    def delete(self, request):
        cart = Cart(request)
        cart.clear()
        return Response(status.HTTP_200_OK)


class RemoveFromCartApi(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Remove product from cart",
        responses={200: "Product removed", 404: "Product not found"},
    )
    def delete(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product.id)
        return Response(cart, status=status.HTTP_200_OK)
