from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from model_bakery import baker

from xshop.core.utils import UserGroup
from xshop.shops.models import Shop
from xshop.users.models import (
    Cashier,
    Customer,
    DataEntryClerk,
    GeneralManager,
    Manager,
    User,
)


@tag("usermodel")
class UserTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
            email="ahmed@shahwan.me",
            password="foo",
        )
        self.user1 = baker.make(User, mobile="01010092182")

    def test_created_user_attrs(self):
        self.assertEqual(self.user.mobile, "+201010092181")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertIsNone(self.user.username)
        self.assertTrue(self.user.check_password("foo"))
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
        superuser = User.objects.create_superuser("+201010092183", "foo")
        self.assertEqual(str(superuser.mobile), "+201010092183")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertIsNone(superuser.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                mobile="+201010092181", password="foo", is_superuser=False
            )

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "Ahmed")

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Ahmed Loay Shahwan")

    def test_str(self):
        self.assertEqual(str(self.user), "01010092181")

    def test_repr(self):
        # user with name
        self.assertEqual(
            self.user.__repr__(),
            f"<User {self.user.id}: {str(self.user)} - {self.user.name}>",
        )
        # user without name
        self.assertEqual(
            self.user1.__repr__(),
            f"<User {self.user1.id}: {str(self.user1)}>",
        )

    def test_token_created_on_user_creation(self):
        self.assertIsNotNone(self.user.auth_token)


@tag("customermodel")
class CustomerTests(TestCase):
    def setUp(self) -> None:
        self.customer = baker.make(Customer, mobile="+201010092181")

    def test_created_customer_attrs(self):
        self.assertEqual(self.customer.mobile, "+201010092181")
        self.assertTrue(self.customer.is_active)
        self.assertFalse(self.customer.is_staff)
        self.assertFalse(self.customer.is_superuser)
        self.assertIsNone(self.customer.username)
        self.assertEqual(Customer.objects.count(), 1)

    def test_customer_added_to_customer_group(self):
        self.assertEqual(self.customer.groups.count(), 1)
        self.assertEqual(self.customer.groups.first().name, UserGroup.CUSTOMER)


@tag("cashiermodel")
class CashierTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="+201010092181")
        self.cashier = baker.make(Cashier, mobile="+201010092181",
                                  shop=self.shop)

    def test_created_cashier_attrs(self):
        self.assertEqual(self.cashier.mobile, "+201010092181")
        self.assertTrue(self.cashier.is_active)
        self.assertFalse(self.cashier.is_staff)
        self.assertFalse(self.cashier.is_superuser)
        self.assertEqual(self.cashier.shop, self.shop)
        self.assertIsNone(self.cashier.username)
        self.assertEqual(Cashier.objects.count(), 1)

    def test_valid_err_if_noshop_with_Cashier(self):
        with self.assertRaises(ValidationError):
            self.user1 = baker.make(Cashier, mobile="+201010092182")

    def test_cashier_added_to_cashier_group(self):
        self.assertEqual(self.cashier.groups.count(), 1)
        self.assertEqual(self.cashier.groups.first().name, UserGroup.CASHIER)


@tag("decmodel")
class DataEntryClerkTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="+201010092181")
        self.dec = baker.make(DataEntryClerk, mobile="+201010092181",
                              shop=self.shop)

    def test_create_dec(self):
        self.assertEqual(self.dec.mobile, "+201010092181")
        self.assertTrue(self.dec.is_active)
        self.assertFalse(self.dec.is_staff)
        self.assertFalse(self.dec.is_superuser)
        self.assertEqual(self.dec.shop, self.shop)
        self.assertIsNone(self.dec.username)
        self.assertEqual(DataEntryClerk.objects.count(), 1)
    
    def test_valid_err_if_noshop_with_DEC(self):
        with self.assertRaises(ValidationError):
            self.user1 = baker.make(DataEntryClerk, mobile="+201010092182")

    def test_dec_added_to_dec_group(self):
        self.assertEqual(self.dec.groups.count(), 1)
        self.assertEqual(self.dec.groups.first().name, UserGroup.DATA_ENTRY_CLERK)


@tag("managermodel")
class ManagerTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="+201010092181")
        self.manager = baker.make(Manager, mobile="+201010092181",
                                  shop=self.shop)

    def test_create_manager(self):
        self.assertEqual(self.manager.mobile, "+201010092181")
        self.assertTrue(self.manager.is_active)
        self.assertFalse(self.manager.is_staff)
        self.assertFalse(self.manager.is_superuser)
        self.assertEqual(self.manager.shop, self.shop)
        self.assertIsNone(self.manager.username)
        self.assertEqual(Manager.objects.count(), 1)
    
    def test_valid_err_if_noshop_with_manager(self):
        with self.assertRaises(ValidationError):
            self.user1 = baker.make(Manager, mobile="+201010092182")

    def test_manager_added_to_manager_group(self):
        self.assertEqual(self.manager.groups.count(), 1)
        self.assertEqual(self.manager.groups.first().name, UserGroup.MANAGER)


@tag("gmmodel")
class GeneralManagerTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="01093862826", name="gm_shop")
        self.gm = baker.make(GeneralManager, mobile="+201010092181", shop=self.shop)

    def test_created_general_manager_attrs(self):
        self.assertEqual(self.gm.mobile, "+201010092181")
        self.assertTrue(self.gm.is_active)
        self.assertFalse(self.gm.is_staff)
        self.assertEqual(self.gm.shop, self.shop)
        self.assertFalse(self.gm.is_superuser)
        self.assertIsNone(self.gm.username)
        self.assertEqual(GeneralManager.objects.count(), 1)
    
    def test_valid_err_if_noshop_with_gm(self):
        with self.assertRaises(ValidationError):
            self.user1 = baker.make(GeneralManager, mobile="+201010092182")

    def test_gm_added_to_gm_group(self):
        self.assertEqual(self.gm.groups.count(), 1)
        self.assertEqual(self.gm.groups.first().name, UserGroup.GENERAL_MANAGER)
