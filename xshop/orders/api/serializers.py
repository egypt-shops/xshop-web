from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "shop", "paid")

    def validate(self, attrs):
        if attrs.get("user") is None:
            raise ValidationError({"user": "invalid, must provide user"})

        if attrs.get("shop") is None:
            raise ValidationError({"shop": "invalid, must provide shop"})
        return attrs


class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    order = OrderSerializer
