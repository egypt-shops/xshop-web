from django.test import TestCase
from model_bakery import baker
from rest_framework.authtoken.models import Token

from ..models import User


class TokenCreationTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
            email="ahmed@shahwan.me",
        )

    def test_token_created_on_user_creation(self):
        self.assertIsNotNone(Token.objects.get(user=self.user))
