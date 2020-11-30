from django.test import Client, TestCase, tag
from django.urls import reverse
from model_bakery import baker

from xshop.shops.models import Shop
from xshop.users.models import Cashier, GeneralManager


@tag("managerview")
class ManagerTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse("dashboard:general_manager")
        self.client = Client()

    def test_manager_can_view(self):
        shop = baker.make(Shop, mobile="01559788591")
        user = baker.make(GeneralManager, mobile="01559788591", shop=shop)
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
        user = baker.make(Cashier, mobile="01559788591")
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)
