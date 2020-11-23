from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.users.models import User


class TokenApiTests(APITestCase):
    def setUp(self):
        self.user = baker.make(User, mobile="01010092181", name="Ahmed Loay Shahwan",)
        self.user.set_password("test")
        self.user.save()
        self.client = APIClient()
        self.url = reverse("users_api:token")

    def test_token_desired_scenario(self):
        resp = self.client.post(
            self.url, {"mobile": self.user.mobile, "password": "test"}
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        user = resp.json().get("user")
        self.user.refresh_from_db()

        self.assertIsNotNone(resp.json().get("token"))
        self.assertIsNotNone(user)
        self.assertEqual(self.user.name, user.get("name"))
        self.assertEqual(self.user.email, user.get("email"))
        self.assertEqual(self.user.type, user.get("type"))
        self.assertEqual(self.user.mobile, user.get("mobile"))

    def test_token_with_nonexistant_mobile(self):
        resp = self.client.post(self.url, {"mobile": "01011698551", "password": "test"})

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json().get("mobile")[0], "user with this mobile does not exist"
        )

    def test_token_with_wrong_password(self):
        resp = self.client.post(
            self.url, {"mobile": self.user.mobile, "password": "sfsdafasdfsad"}
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.json().get("password")[0], "Invalid")
