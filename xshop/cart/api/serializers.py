from django.core.exceptions import ValidationError
from rest_framework import serializers

from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    override_quantity = serializers.BooleanField(default=False)

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        quantity = attrs.get("quantity")
        override_quantity = attrs.get("override_quantity")

        try:
            product = Product.objects.get(id=product_id)
            serialized_product = ProductSerializer(product)
        except Product.DoesNotExist:
            raise ValidationError({"product_id": "Not found"})
        if product.stock < quantity:
            raise ValidationError({"quantity": f"Invalid. Available {product.stock}"})
        if quantity > 1 and not override_quantity:
            raise ValidationError({"override_quantity": "Invalid. quantity > 1"})

        attrs["product"] = serialized_product.data
        return attrs
