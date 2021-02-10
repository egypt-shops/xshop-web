from django.contrib.auth import get_user_model
from django.test import tag
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.exceptions import ValidationError

from xshop.products.models import Product

User = get_user_model()


@tag("cartapi")
class CartApiTests(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010101010", name="Test User")
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.product = baker.make(Product, stock=10)

        self.payload = {"product_id": self.product.id, "quantity": 1, "actions": "add"}

        self.client = APIClient()
        self.cart_url = reverse("cart_api:cart_operations")

    def test_get_cart_not_authenticated(self):
        resp = self.client.get(self.cart_url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get(self.cart_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_add_product_to_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(resp.data), 0)

    def test_add_none_existing_product_to_cart(self):
        self.payload["product_id"] = 10
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_add_product_id_equal_none(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_update_product_in_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.cart_url, data=self.payload)
        self.payload["quantity"] = 5
        self.payload["actions"] = "patch"
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(resp.data), 0)

    def test_update_product_quantity_greater_than_stock(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.cart_url, data=self.payload)
        self.payload["quantity"] = 123
        self.payload["actions"] = "patch"
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "quantity", raise_exception=True)

    def test_update_none_existing_product(self):
        self.payload["product_id"] = 3
        self.payload["actions"] = "patch"
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "quantity", raise_exception=True)

    def test_remove_product_from_cart(self):
        self.client.post(self.cart_url, data=self.payload)
        self.payload["actions"] = "remove"
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_remove_none_existing_product_from_cart(self):
        self.payload["product_id"] = 1234
        self.payload["actions"] = "remove"
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_clear_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.cart_url, data=self.payload)
        self.payload["actions"] = "clear"
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
