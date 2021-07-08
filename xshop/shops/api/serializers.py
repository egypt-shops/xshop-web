from rest_framework import serializers

from xshop.products.models import Product

from ..models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("id", "name", "mobile", "dashboard_modules", "subdomain")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "barcode")
