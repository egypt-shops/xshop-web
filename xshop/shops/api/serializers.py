from rest_framework import serializers

from ..models import Shop
from xshop.products.models import Product


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("id", "name", "mobile", "dashboard_modules")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "barcode")
