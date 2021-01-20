from django.test import TestCase, tag
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from xshop.products.models import Product
from xshop.cart.api.serializers import AddToCartSerializer


@tag("cartserializer")
class CartSerializerTest(TestCase):
    def setUp(self) -> None:
        self.product = baker.make(Product, stock=1)
        self.product2 = baker.make(Product, stock=15)

        self.payload = {
            "product_id": self.product.id,
            "quantity": 1,
            "override_quantity": False,
        }

    def test_correct_data(self):
        serializer = AddToCartSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_serializer_product_not_found(self):
        self.payload["product_id"] = 10
        serializer = AddToCartSerializer(data=self.payload)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    def test_serializer_invalid_quantity(self):
        self.payload["quantity"] = 10
        self.payload["override_quantity"] = True
        serializer = AddToCartSerializer(data=self.payload)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    def test_serializer_invalid_override_quantity(self):
        self.payload["product_id"] = self.product2.id
        self.payload["quantity"] = 10
        serializer = AddToCartSerializer(data=self.payload)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)
