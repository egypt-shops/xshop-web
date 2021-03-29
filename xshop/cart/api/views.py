from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg2.utils import swagger_auto_schema


from .serializers import CartSerializer
from ..cart import Cart


class CartApi(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add product to cart",
        request_body=CartSerializer,
        responses={
            200: CartSerializer,
            400: [{"product_id": "Not found"}, {"quantity": "Invalid"}],
        },
    )
    def post(self, request):
        cart = Cart(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data.get("actions")

        if action == "add":
            product = serializer.validated_data.get("product")
            cart.add(product=product)
            return Response(cart)

        elif action == "patch":
            product = serializer.validated_data.get("product")

            cart.update(
                product=product,
                quantity=serializer.validated_data.get("quantity"),
            )
            return Response(cart)

        elif action == "remove":
            product_id = serializer.validated_data.get("product_id")
            cart.remove(product_id)
            return Response(cart, status=status.HTTP_200_OK)

        elif action == "clear":
            cart.clear()
            return Response(status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="get cart's product", responses={200: CartSerializer}
    )
    def get(self, request):
        cart = Cart(request)

        return Response(cart)
