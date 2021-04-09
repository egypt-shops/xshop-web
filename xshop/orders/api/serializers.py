from rest_framework import serializers

from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "shop", "paid")


class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    order = OrderSerializer
