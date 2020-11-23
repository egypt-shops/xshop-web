from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.users.models import User
from xshop.shops.models import Shop
from xshop.products.models import Product


class ShopsApiTests(APITestCase):
    def detail_url(self, shop_id):
        return reverse("shops_api:shop_detail", args=[shop_id])

    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
        )
        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.shop2 = baker.make(Shop, mobile=self.user.mobile, name="shop2")
        self.product1 = baker.make(
            Product,
            name="Prod1",
            barcode="12345",
            stock=15,
            price=12,
            added_by=self.user,
            shop=self.shop1,
        )
        self.client = APIClient()
        self.list_url = reverse("shops_api:shop_list")

    def test_retreive_shops(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_retreive_shop_detail(self):
        resp = self.client.get(self.detail_url(self.shop1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], self.shop1.name)
        self.assertEqual(resp.data["mobile"], self.shop1.mobile)

    def test_retreive_none_existing_shop(self):
        resp = self.client.get(self.detail_url(154))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)

    def test_retrieve_searched_product_by_name(self):
        url = "{url}?{filter}={value}".format(
            url=reverse("shops_api:product_list"),
            filter="search",
            value=self.product1.name,
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_searched_product_by_barcode(self):
        url = "{url}?{filter}={value}".format(
            url=reverse("shops_api:product_list"),
            filter="search",
            value=self.product1.barcode,
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_non__existing_product(self):
        resp = self.client.get(self.detail_url(102))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)
