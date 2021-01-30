from django.test import TestCase, tag
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from xshop.products.models import Product
from xshop.cart.api.serializers import CartSerializer


@tag("cartserializer")
class CartSerializerTest(TestCase):
    def setUp(self) -> None:
        self.product = baker.make(Product, stock=1)
        self.product2 = baker.make(Product, stock=15)

        self.payload = {"product_id": self.product.id, "quantity": 1, "actions": "add"}

    def test_correct_data(self):
        serializer = CartSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_serializer_product_not_found(self):
        self.payload["product_id"] = 10
        serializer = CartSerializer(data=self.payload)
        self.assertRaisesMessage(
            ValidationError, "Not found", serializer.is_valid, raise_exception=True
        )

    def test_serializer_None_quantity(self):
        self.payload["quantity"] = None
        self.payload["actions"] = "patch"
        serializer = CartSerializer(data=self.payload)
        self.assertRaisesMessage(
            ValidationError,
            "quantity",
            serializer.is_valid,
            raise_exception=True,
        )

    def test_serializer_invalid_quantity(self):
        self.payload["quantity"] = 10
        self.payload["actions"] = "patch"
        serializer = CartSerializer(data=self.payload)
        self.assertRaisesMessage(
            ValidationError,
            f"Invalid. available stock {self.product.stock}",
            serializer.is_valid,
            raise_exception=True,
        )
