from django.test import TestCase, tag
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from xshop.users.models import User
from xshop.shops.models import Shop
from xshop.orders.api.serializers import CheckoutSerializer, OrderSerializer


@tag("checkoutserializer")
class CheckoutSerializerTest(TestCase):
    def setUp(self) -> None:
        self.payload = {"address": "zagazig"}

    def test_correct_data(self):
        serializer = CheckoutSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(raise_exception=True))


@tag("orderserializer")
class OrderSerializerTest(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="01010101010", name="xshop")
        self.user = baker.make(User, mobile="01020202020")

        self.payload = {"user": self.user.pk, "shop": self.shop.pk}

    def test_correct_data(self):
        serializer = OrderSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertFalse(serializer.validated_data.get("paid"))

    def test_order_shop_not_found(self):
        self.payload["shop"] = 10
        serializer = OrderSerializer(data=self.payload)
        self.assertRaisesMessage(
            ValidationError,
            "object does not exist",
            serializer.is_valid,
            raise_exception=True,
        )

    def test_order_user_not_found(self):
        self.payload["user"] = 10
        serializer = OrderSerializer(data=self.payload)
        self.assertRaisesMessage(
            ValidationError,
            "object does not exist",
            serializer.is_valid,
            raise_exception=True,
        )

    def test_order_paid_is_True(self):
        self.payload["paid"] = True
        serializer = OrderSerializer(data=self.payload)
        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.validated_data.get("paid"))
