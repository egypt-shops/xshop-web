from django.contrib.auth import get_user_model
from django.test import tag
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.products.models import Product

User = get_user_model()


@tag("cartapi")
class CartApiTests(APITestCase):
    def remove_product_url(self, product_id):
        return reverse("cart_api:remove_product_from_cart", args=[product_id])

    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010101010", name="Test User")
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.product = baker.make(Product, stock=10)

        self.payload = {
            "product_id": self.product.id,
            "quantity": 3,
            "override_quantity": True,
        }

        self.client = APIClient()
        self.cart_url = reverse("cart_api:add_get_clear_cart")

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
        # self.assertRaises(ValidationError, "product_id")

    def test_add_product_greater_than_stock(self):
        self.payload["quantity"] = 100
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.cart_url, data=self.payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertRaises(ValidationError, "product_id")

    def test_remove_product_from_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.delete(self.remove_product_url(self.product.id))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_remove_none_existing_product_from_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.delete(self.remove_product_url(150))

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertRaises(ValidationError, "product_id")

    def test_clear_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.delete(self.cart_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
