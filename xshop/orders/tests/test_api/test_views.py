from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.orders.models import Order
from xshop.shops.models import Shop
from xshop.users.models import User
from xshop.products.models import Product


class OrderApiTests(APITestCase):
    def detail_patch_url(self, order_id):
        return reverse("orders_api:order_detail_patch", args=[order_id])

    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
        )
        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.order1 = baker.make(Order, user=self.user, shop=self.shop1)
        self.client = APIClient()
        self.url = reverse("orders_api:order_list_create")

    def test_api_can_create_order(self):
        order_data = {"user": self.user.pk, "shop": self.shop1.pk}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["user"], order_data["user"])
        self.assertEqual(resp.data["shop"], order_data["shop"])

    def test_order_api_nonexistent_user(self):
        order_data = {"user": 2, "shop": self.shop1.pk}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_api_nonexistent_shop(self):
        order_data = {"user": self.user.pk, "shop": 1000}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_api_string_user(self):
        order_data = {"user": "invalid", "shop": self.shop1.pk}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_api_string_shop(self):
        order_data = {"user": self.user.pk, "shop": "invalid"}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_existing_order(self):
        resp = self.client.get(self.detail_patch_url(self.order1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], self.order1.id)

    def test_retrieve_none_existing_order(self):
        resp = self.client.get(self.detail_patch_url(102))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)


class CheckoutApiTests(APITestCase):
    def detail_patch_url(self, order_id):
        return reverse("orders_api:checkout_operations", args=[order_id])

    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010101010", name="Test User")
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()

        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.product = baker.make(Product, shop=self.shop1, stock=10)

        self.payload = {"product_id": self.product.id, "quantity": 1, "actions": "add"}

        self.client = APIClient()
        self.cart_url = reverse("cart_api:cart_operations")

        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.cart_url, data=self.payload)

        self.url = reverse("orders_api:checkout")

    def test_api_can_checkout(self):
        order_data = {"address": "zagazig"}
        resp = self.client.post(self.url, order_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["order_data"]["user_pk"], self.user.pk)
        self.assertEqual(resp.data["order_data"]["shop_pk"], self.shop1.pk)
        self.assertEqual(resp.data["order_data"]["item_count"], 1)
        self.assertEqual(resp.data["address"], "zagazig")
