from django.test import Client, TestCase, tag
from django.urls import reverse
from rest_framework import status


@tag("homeview")
class HomeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("pages:home")

    def test_home_uses_desired_template(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(resp, "pages/home.html")


class LoginTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("login")

    def test_login_uses_desired_template(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(resp, "registration/login.html")
