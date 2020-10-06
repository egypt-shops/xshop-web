from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User
from rest_framework.test import APIClient
from model_bakery import baker


class LoginAPITests(APITestCase):
    def setUp(self):

        self.user = baker.make(User, mobile="01010092181", name="Ahmed Loay Shahwan",)
        self.user.set_password("test")
        self.user.save()
        self.client = APIClient()
        self.url = reverse("users:login")

    def test_login_returns_token(self):
        resp = self.client.post(
            self.url, {"mobile": self.user.mobile, "password": "test"}
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(resp.json().get("token"))

    def test_login_with_nonexistant_mobile(self):
        resp = self.client.post(self.url, {"mobile": "01011698551", "password": "test"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json().get("mobile")[0], "user with this mobile does not exist"
        )

    def test_login_with_wrong_password(self):
        resp = self.client.post(
            self.url, {"mobile": self.user.mobile, "password": "sfsdafasdfsad"}
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json().get("password")[0], "Invalid")
