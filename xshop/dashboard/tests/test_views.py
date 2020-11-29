from django.urls import reverse
from django.test import TestCase, Client, tag

from model_bakery import baker
from xshop.shops.models import Shop
from xshop.users.models import User


@tag("managerview")
class ManagerTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse("dashboard:general_manager")
        self.client = Client()

    def test_manager_can_view(self):
        shop = baker.make(Shop, mobile="01559788591")
        user = baker.make(User, mobile="01559788591", type=["MANAGER"], shop=shop)
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_manager_page_requires_login(self):
        resp = self.client.get(self.url)
        self.assertRedirects(
            resp,
            f"{reverse('users:login')}?next={reverse('dashboard:general_manager')}",
        )

    def test_manager_page_allowed_only_for_managers(self):
        user = baker.make(User, mobile="01559788591", type=["CASHIER"])
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)
