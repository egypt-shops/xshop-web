from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import Group
from model_bakery import baker

from xshop.core.utils import UserGroup
from xshop.shops.models import Shop
from xshop.users.models import Cashier, DataEntryClerk, GeneralManager


class CreateGroupsTests(TestCase):
    def test_retrieve_existing_groups(self):
        self.assertEqual(Group.objects.all().count(), 0)
        call_command("create_groups")
        self.assertEqual(Group.objects.all().count(), 5)
        self.assertTrue(Group.objects.get(name=UserGroup.CUSTOMER))
        self.assertTrue(Group.objects.get(name=UserGroup.GENERAL_MANAGER))
        self.assertTrue(Group.objects.get(name=UserGroup.CASHIER))
        self.assertTrue(Group.objects.get(name=UserGroup.MANAGER))
        self.assertTrue(Group.objects.get(name=UserGroup.DATA_ENTRY_CLERK))


class GmPermissionsTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="01093862826", name="gm_shop")
        self.gm = baker.make(GeneralManager, mobile="+201010092181", shop=self.shop)

    def test_command(self):
        self.assertEqual(self.gm.groups.first().permissions.all().count(), 0)

        call_command("gm_permissions")

        self.assertEqual(self.gm.groups.first().permissions.all().count(), 32)
        # check shops permissions
        self.assertTrue(self.gm.has_perm("shops.view_shop"))
        self.assertTrue(self.gm.has_perm("shops.change_shop"))
        self.assertFalse(self.gm.has_perm("shops.add_shop"))
        self.assertFalse(self.gm.has_perm("shops.delete_shop"))
        # check general manager permissions
        self.assertTrue(self.gm.has_perm("users.view_generalmanager"))
        self.assertTrue(self.gm.has_perm("users.change_generalmanager"))
        self.assertFalse(self.gm.has_perm("users.add_generalmanager"))
        self.assertFalse(self.gm.has_perm("users.delete_generalmanager"))
        # check manager permissions
        self.assertTrue(self.gm.has_perm("users.view_manager"))
        self.assertTrue(self.gm.has_perm("users.change_manager"))
        self.assertTrue(self.gm.has_perm("users.add_manager"))
        self.assertTrue(self.gm.has_perm("users.delete_manager"))
        # check data entry clerk permissions
        self.assertTrue(self.gm.has_perm("users.view_dataentryclerk"))
        self.assertTrue(self.gm.has_perm("users.change_dataentryclerk"))
        self.assertTrue(self.gm.has_perm("users.add_dataentryclerk"))
        self.assertTrue(self.gm.has_perm("users.delete_dataentryclerk"))
        # check cashier permissions
        self.assertTrue(self.gm.has_perm("users.view_cashier"))
        self.assertTrue(self.gm.has_perm("users.change_cashier"))
        self.assertTrue(self.gm.has_perm("users.add_cashier"))
        self.assertTrue(self.gm.has_perm("users.delete_cashier"))
        # check product permissions
        self.assertTrue(self.gm.has_perm("products.view_product"))
        self.assertTrue(self.gm.has_perm("products.change_product"))
        self.assertTrue(self.gm.has_perm("products.add_product"))
        self.assertTrue(self.gm.has_perm("products.delete_product"))
        # check order permissions
        self.assertTrue(self.gm.has_perm("orders.view_order"))
        self.assertTrue(self.gm.has_perm("orders.change_order"))
        self.assertTrue(self.gm.has_perm("orders.add_order"))
        self.assertTrue(self.gm.has_perm("orders.delete_order"))
        # check order item permissions
        self.assertTrue(self.gm.has_perm("orders.view_orderitem"))
        self.assertTrue(self.gm.has_perm("orders.change_orderitem"))
        self.assertTrue(self.gm.has_perm("orders.add_orderitem"))
        self.assertTrue(self.gm.has_perm("orders.delete_orderitem"))
        # check invoice permissions
        self.assertTrue(self.gm.has_perm("invoices.view_invoice"))
        self.assertTrue(self.gm.has_perm("invoices.change_invoice"))
        self.assertTrue(self.gm.has_perm("invoices.add_invoice"))
        self.assertTrue(self.gm.has_perm("invoices.delete_invoice"))


class DECPermissionsTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="01093862826", name="dec_shop")
        self.dec = baker.make(DataEntryClerk, mobile="+201010092181", shop=self.shop)

    def test_command(self):
        self.assertEqual(self.dec.groups.first().permissions.all().count(), 0)

        call_command("dec_permissions")

        self.assertEqual(self.dec.groups.first().permissions.all().count(), 3)
        self.assertTrue(self.dec.has_perm("products.view_product"))
        self.assertTrue(self.dec.has_perm("products.change_product"))
        self.assertTrue(self.dec.has_perm("products.add_product"))
        self.assertFalse(self.dec.has_perm("products.delete_product"))


class CashierPermissionsTests(TestCase):
    def setUp(self) -> None:
        self.shop = baker.make(Shop, mobile="01093862826", name="cashier_shop")
        self.cashier = baker.make(Cashier, mobile="+201010092181", shop=self.shop)

    def test_command(self):
        self.assertEqual(self.cashier.groups.first().permissions.all().count(), 0)

        call_command("cashier_permissions")

        self.assertEqual(self.cashier.groups.first().permissions.all().count(), 5)
        # check order permissions
        self.assertTrue(self.cashier.has_perm("orders.view_order"))
        self.assertFalse(self.cashier.has_perm("orders.change_order"))
        self.assertTrue(self.cashier.has_perm("orders.add_order"))
        self.assertFalse(self.cashier.has_perm("orders.delete_order"))
        # check order item permissions
        self.assertTrue(self.cashier.has_perm("orders.view_orderitem"))
        self.assertFalse(self.cashier.has_perm("orders.change_orderitem"))
        self.assertTrue(self.cashier.has_perm("orders.add_orderitem"))
        self.assertFalse(self.cashier.has_perm("orders.delete_orderitem"))
        # check invoice permissions
        self.assertTrue(self.cashier.has_perm("invoices.view_invoice"))
        self.assertFalse(self.cashier.has_perm("invoices.change_invoice"))
        self.assertFalse(self.cashier.has_perm("invoices.add_invoice"))
        self.assertFalse(self.cashier.has_perm("invoices.delete_invoice"))
