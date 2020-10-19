from django.test import TestCase, tag
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from xshop.users.models import Cashier, Customer, DataEntryClerk, Manager, SubManager


class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(mobile="+201010092181", password="foo")
        self.assertEqual(user.mobile, "+201010092181")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        self.assertTrue(user.check_password("foo"))
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(mobile="")
        with self.assertRaises(TypeError):
            User.objects.create_user(password="")
        with self.assertRaises(ValidationError):
            User.objects.create_user(mobile="123", password="foo")
        with self.assertRaises(ValidationError):
            User.objects.create_user(mobile="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("+201010092181", "foo")
        self.assertEqual(admin_user.mobile, "+201010092181")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                mobile="+201010092181", password="foo", is_superuser=False
            )


@tag("cmt")
class CustomerManagerTests(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create(mobile="+201010092181", password="foo")
        self.assertEqual(customer.mobile, "+201010092181")
        self.assertEqual(customer.type, "CUSTOMER")
        self.assertTrue(customer.is_active)
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_superuser)
        self.assertIsNone(customer.username)


@tag("camt")
class CashierManagerTests(TestCase):
    def test_create_customer(self):
        cashier = Cashier.objects.create(mobile="+201010092181", password="foo")
        self.assertEqual(cashier.mobile, "+201010092181")
        self.assertEqual(cashier.type, "CASHIER")
        self.assertTrue(cashier.is_active)
        self.assertFalse(cashier.is_staff)
        self.assertFalse(cashier.is_superuser)
        self.assertIsNone(cashier.username)


@tag("decmt")
class DataEntryClerkManagerTests(TestCase):
    def test_create_customer(self):
        dec = DataEntryClerk.objects.create(mobile="+201010092181", password="foo")
        self.assertEqual(dec.mobile, "+201010092181")
        self.assertEqual(dec.type, "DATA_ENTRY_CLERK")
        self.assertTrue(dec.is_active)
        self.assertFalse(dec.is_staff)
        self.assertFalse(dec.is_superuser)
        self.assertIsNone(dec.username)


@tag("smmt")
class SubManagerManagerTests(TestCase):
    def test_create_customer(self):
        sub_manager = SubManager.objects.create(mobile="+201010092181", password="foo")
        self.assertEqual(sub_manager.mobile, "+201010092181")
        self.assertEqual(sub_manager.type, "SUB_MANAGER")
        self.assertTrue(sub_manager.is_active)
        self.assertFalse(sub_manager.is_staff)
        self.assertFalse(sub_manager.is_superuser)
        self.assertIsNone(sub_manager.username)


@tag("mmt")
class ManagerManagerTests(TestCase):
    def test_create_customer(self):
        manager = Manager.objects.create(mobile="+201010092181", password="foo")
        self.assertEqual(manager.mobile, "+201010092181")
        self.assertEqual(manager.type, "MANAGER")
        self.assertTrue(manager.is_active)
        self.assertFalse(manager.is_staff)
        self.assertFalse(manager.is_superuser)
        self.assertIsNone(manager.username)
