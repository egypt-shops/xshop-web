from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Order
from .serializers import OrderSerializer


class OrderListCreateApi(APIView):
    serializer_class = OrderSerializer

    @extend_schema(
        description="List all orders",
        responses={200: "orders list"},
    )
    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create new Order",
        request=OrderSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_order = serializer.save()
        return Response(self.serializer_class(new_order).data)


class OrderDetailPatchApi(APIView):
    serializer_class = OrderSerializer

    @extend_schema(
        description="Get Order details",
        responses={200: OrderSerializer, 404: "Order not found"},
    )
    def get(self, request, order_id):
        try:
            orders = Order.objects.get(id=order_id)

            serializer = self.serializer_class(orders, many=False)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Patch existing Order",
        request=OrderSerializer,
        responses={404: "Order does not exist"},
    )
    def patch(self, request, order_id):
        try:
            orders = Order.objects.get(id=order_id)
            serializer = self.serializer_class(orders, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_order = serializer.save()
            return Response(self.serializer_class(updated_order).data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
