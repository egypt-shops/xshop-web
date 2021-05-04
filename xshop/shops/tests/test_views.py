from django.test import Client, TestCase, tag
from django.urls import reverse
from model_bakery import baker

from xshop.shops.models import Shop
from xshop.users.models import User


@tag("cartview")
class CartTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010101010",
            name="Hatem",
        )
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.shop = baker.make(Shop, mobile="01222222222")
        self.client = Client()
        self.url = reverse("shop:shop_details", kwargs={"shop_id": self.shop.id})

    def test_get_shop_details_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)

    def test_get_shop_details(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
