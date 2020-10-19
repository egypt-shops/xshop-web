from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from model_bakery import baker
from django.contrib.auth import get_user_model

from ..models import Product

User = get_user_model()


class ProductApiTests(APITestCase):
    def detail_patch_url(self, product_id):
        return reverse("core_api:product_detail_patch", args=[product_id])

    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010092181", name="Ahmed Loay Shahwan",)
        self.user.save()
        self.product1 = baker.make(
            Product, name="Prod1", stock=15, price=12, added_by=self.user
        )
        self.product2 = baker.make(
            Product, name="Prod2", stock=10, price=41, added_by=self.user
        )
        self.product1.save()
        self.product2.save()
        self.client = APIClient()
        self.list_create_url = reverse("core_api:product_list_create")

    def test_get_all_products(self):
        resp = self.client.get(self.list_create_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_create_valid_product_with_price(self):
        product = {
            "name": "test",
            "stock": 14,
            "price": "17.00",
            "added_by": self.user.id,
        }
        resp = self.client.post(self.list_create_url, product)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], product["name"])
        self.assertEqual(resp.data["stock"], product["stock"])
        self.assertEqual(resp.data["price"], product["price"])

    def test_create_valid_product_without_price(self):
        product = {"name": "test", "stock": 14, "added_by": self.user.id}
        resp = self.client.post(self.list_create_url, product)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], product["name"])
        self.assertEqual(resp.data["stock"], product["stock"])
        self.assertEqual(resp.data["price"], "0.00")

    def test_create_product_with_string_stock(self):
        product = {"name": "test", "stock": "test", "added_by": self.user.id}
        resp = self.client.post(self.list_create_url, product)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("A valid integer is required." in resp.data["stock"])

    def test_create_product_with_blank_name(self):
        product = {"name": "", "stock": 15, "added_by": self.user.id}
        resp = self.client.post(self.list_create_url, product)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("This field may not be blank." in resp.data["name"])

    def test_create_product_with_null_user(self):
        product = {"name": "test", "stock": 15}
        resp = self.client.post(self.list_create_url, product)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["added_by"], None)

    def test_retrieve_existing_product(self):
        resp = self.client.get(self.detail_patch_url(self.product1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], self.product1.name)

    def test_retrieve_none_existing_product(self):
        resp = self.client.get(self.detail_patch_url(102))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)

    def test_patch_exiting_product_name(self):
        product_name = {"name": "New"}
        resp = self.client.patch(self.detail_patch_url(self.product1.id), product_name)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data["name"], product_name["name"])

    def test_patch_exiting_product_name_blank(self):
        product_name = {"name": ""}
        resp = self.client.patch(self.detail_patch_url(self.product1.id), product_name)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("This field may not be blank." in resp.data["name"])

    def test_patch_exiting_product_stock(self):
        product_stock = {"stock": 12}
        resp = self.client.patch(self.detail_patch_url(self.product1.id), product_stock)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data["stock"], product_stock["stock"])

    def test_patch_exiting_product_stock_string(self):
        product_stock = {"stock": "pl"}
        resp = self.client.patch(self.detail_patch_url(self.product1.id), product_stock)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("A valid integer is required." in resp.data["stock"])

    def test_patch_exiting_product_price(self):
        product_price = {"price": 25}
        resp = self.client.patch(self.detail_patch_url(self.product1.id), product_price)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data["name"], str(product_price["price"]))
