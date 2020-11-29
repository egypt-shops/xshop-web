from django.test import TestCase, Client, tag
from django.urls import reverse
from model_bakery import baker

from xshop.users.models import User
from xshop.shops.models import Shop


@tag("login")
class LoginTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("users:login")

    def test_login_uses_desired_template(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "registration/login.html")


@tag("redirection")
class RedirectionTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("users:redirection")
        self.shop = baker.make(Shop, mobile="01559788591")

    def test_requires_login(self):
        resp = self.client.get(self.url)
        self.assertRedirects(
            resp, f"{reverse('users:login')}?next={reverse('users:redirection')}"
        )

    def test_superuser_redirected_to_admin_index(self):
        user = baker.make(User, mobile="01559788591", is_superuser=True)
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertTrue(user.is_superuser)
        self.assertRedirects(resp, reverse("admin:index"), 302, 302)

    def test_manager_redirected_to_manager_page(self):
        user = baker.make(User, mobile="01559788591", type=["MANAGER"], shop=self.shop)
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse("dashboard:general_manager"), 302)

    def test_cashier_redirected_to_cashier_page(self):
        user = baker.make(User, mobile="01559788591", type=["CASHIER"], shop=self.shop)
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse("dashboard:cashier"), 302)

    def test_dec_redirected_to_data_entry_page(self):
        user = baker.make(
            User, mobile="01559788591", type=["DATA_ENTRY_CLERK"], shop=self.shop
        )
        self.client.force_login(user)
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse("dashboard:data_entry"), 302)
