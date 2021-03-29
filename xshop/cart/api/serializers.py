from django.core.exceptions import ValidationError
from rest_framework import serializers

from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer

choices = (
    ("add", "Add product to cart"),
    ("patch", "Update product in cart"),
    ("remove", "Remove product from cart"),
    ("clear", "Delete all products in cart"),
)


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1, required=False)
    quantity = serializers.IntegerField(min_value=1, required=False)
    actions = serializers.ChoiceField(choices=choices)

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        quantity = attrs.get("quantity")
        action = attrs.get("actions")

        if action == "clear":
            return attrs

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"product_id": "Not found"})
        if action == "patch" and quantity is None:
            raise ValidationError({"quantity": "invalid, must provide quantity"})
        if action == "patch" and product.stock < quantity:
            raise ValidationError(
                {"quantity": f"Invalid. available stock {product.stock}"}
            )

        attrs["product"] = ProductSerializer(product).data
        return attrs
