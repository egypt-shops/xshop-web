from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework import status
from model_bakery import baker

from xshop.shops.models import Shop
from xshop.users.models import User


@tag("homeview")
class HomeTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
        )
        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.shop2 = baker.make(Shop, mobile=self.user.mobile, name="shop2")
        self.client = Client()
        self.url = reverse("pages:home")

    def test_home_uses_desired_template(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(resp, "pages/home.html")

    def test_retreive_shops(self):
        resp = self.client.get("/")
        self.assertEqual(len(resp.context["shops"]), 2)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Check for logged in user
        self.client.force_login(self.user)
        self.assertEqual(len(resp.context["shops"]), 2)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
