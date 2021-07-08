from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.shops.models import Shop
from xshop.users.models import User


class ShopsApiTests(APITestCase):
    def detail_url(self, shop_id):
        return reverse("shops_api:shop_detail", args=[shop_id])

    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
        )
        self.shop1 = baker.make(
            Shop, mobile=self.user.mobile, name="shop1", subdomain="safnksfj"
        )
        self.shop2 = baker.make(
            Shop, mobile=self.user.mobile, name="shop2", subdomain="sfnsdjkf"
        )
        self.client = APIClient()
        self.list_url = reverse("shops_api:shop_list")

    def test_retreive_shops(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_retreive_shop_detail(self):
        resp = self.client.get(self.detail_url(self.shop1.subdomain))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], self.shop1.name)
        self.assertEqual(resp.data["mobile"], self.shop1.mobile)

    def test_retreive_none_existing_shop(self):
        resp = self.client.get(self.detail_url(154))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
