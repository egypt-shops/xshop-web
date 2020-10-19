from django.test import TestCase

from ..services import (
    user_create,
    customer_create,
    cashier_create,
    data_entry_create,
    manager_create,
    sub_manager_create,
)
from ..models import User


class user_create_test(TestCase):
    def setUp(self) -> None:
        self.user = user_create(
            name="Hatem Mohammed Kamal", mobile="01094862826", password="123qwe!@#"
        )
        self.user1 = user_create(mobile="01010101010", password="123456qwerty")

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "Hatem")

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Hatem Mohammed Kamal")

    def test_str(self):
        self.assertEqual(str(self.user), "01094862826")

    def test_repr(self):
        # user with name
        self.assertEqual(
            self.user.__repr__(),
            f"<User {self.user.id}: {str(self.user)} - {self.user.name}>",
        )
        # user without name
        self.assertEqual(
            self.user1.__repr__(), f"<User {self.user1.id}: {str(self.user1)}>",
        )

    def test_token_created_on_user_creation(self):
        self.assertIsNotNone(self.user.auth_token)


class test_customer_user(TestCase):
    def setUp(self) -> None:
        self.user2 = customer_create(
            name="Hatem Mhammed Kamal",
            mobile="01093862826",
            password="121qwe!@#",
            email="hmmk@g.com",
        )

    def test_customer_user_type(self):
        self.assertEqual(self.user2.type, User.Types.CUSTOMER)

    def test_repr_customer(self):
        self.assertEqual(
            self.user2.__repr__(),
            f"<User {self.user2.id}: {str(self.user2)} - {self.user2.name}>",
        )


class test_cashier_user(TestCase):
    def setUp(self) -> None:
        self.user2 = cashier_create(
            name="Hatem Mhammed Kamal",
            mobile="01093862826",
            password="121qwe!@#",
            email="hmmk@g.com",
        )

    def test_customer_user_type(self):
        self.assertEqual(self.user2.type, User.Types.CASHIER)


class test_data_entry_user(TestCase):
    def setUp(self) -> None:
        self.user2 = data_entry_create(
            name="Hatem Mhammed Kamal",
            mobile="01093862826",
            password="121qwe!@#",
            email="hmmk@g.com",
        )

    def test_customer_user_type(self):
        self.assertEqual(self.user2.type, User.Types.DATA_ENTRY_CLERK)


class test_manager_user(TestCase):
    def setUp(self) -> None:
        self.user2 = manager_create(
            name="Hatem Mhammed Kamal",
            mobile="01093862826",
            password="121qwe!@#",
            email="hmmk@g.com",
        )

    def test_customer_user_type(self):
        self.assertEqual(self.user2.type, User.Types.MANAGER)


class test_sub_manager_user(TestCase):
    def setUp(self) -> None:
        self.user2 = sub_manager_create(
            name="Hatem Mhammed Kamal",
            mobile="01093862826",
            password="121qwe!@#",
            email="hmmk@g.com",
        )

    def test_customer_user_type(self):
        self.assertEqual(self.user2.type, User.Types.SUB_MANAGER)
