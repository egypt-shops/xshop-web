from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models import Order
from xshop.shops.models import Shop
from xshop.users.models import User
from xshop.shops.api.serializers import ShopSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "shop", "paid")

    def validate(self, attrs):
        if attrs.get('user') == None:
            raise ValidationError({'user': "invalid, must provide user"})
        
        if attrs.get('shop') == None:
            raise ValidationError({"shop": "invalid, must provide shop"})        
        return attrs


class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    order = OrderSerializer
