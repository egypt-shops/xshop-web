from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.users.models import User
from xshop.shops.models import Shop


class ShopsApiTests(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010092181", name="Ahmed Loay Shahwan",)
        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.shop2 = baker.make(Shop, mobile=self.user.mobile, name="shop2")
        self.client = APIClient()
        self.list_url = reverse("shops_api:shop_list")

    def test_retreive_shops(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
