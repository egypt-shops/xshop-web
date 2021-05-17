from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.core.exceptions import PermissionDenied
from model_bakery import baker

from xshop.users.models import Cashier, Manager, User
from xshop.shops.models import Shop
from xshop.orders.models import Order
from ..admin import InvoiceAdmin
from ..models import Invoice


class MockRequest:
    GET = ""

    def get(self):
        request_factory = RequestFactory()
        return request_factory.get("/admin")


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class InvoiceAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = InvoiceAdmin(Invoice, self.site)

        # shops
        self.shop_test = baker.make(Shop, mobile="01010092182")
        self.shop = baker.make(Shop, mobile="01010092183")
        self.shop1 = baker.make(Shop, mobile="01010092184")

        # orders
        self.order_test = baker.make(Order, shop=self.shop_test)
        self.order = baker.make(Order, shop=self.shop)

        # invoice
        self.invoice_test = baker.make(Invoice, order=self.order_test)
        self.invoice = baker.make(Invoice, order=self.order)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)
        self.cashier = baker.make(Cashier, mobile="01010092183", shop=self.shop)
        self.cashier1 = baker.make(Cashier, mobile="01010092184", shop=self.shop1)
        self.manager = baker.make(Manager, mobile="01010092186", shop=self.shop)
        self.manager1 = baker.make(Manager, mobile="01010092187", shop=self.shop1)
        self.test_user = baker.make(User, mobile="01010092185")

        # requests
        self.request_super = MockRequest()
        self.request_super.user = self.superuser

        self.request_cashier = MockRequest()
        self.request_cashier.user = self.cashier

        self.request_manager = MockRequest()
        self.request_manager.user = self.manager

        self.request_no_invoice = MockRequest()
        self.request_no_invoice.user = self.cashier1

        self.request_no_invoice1 = MockRequest()
        self.request_no_invoice1.user = self.manager1

        self.request_test_user = MockRequest()
        self.request_test_user.user = self.test_user

        # attr values

    def test_superuser_invoice_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_super).order_by("-id")),
            list(Invoice.objects.all().order_by("-id")),
        )

    def test_cashier_invoice_queryset(self):
        orders = Order.objects.filter(shop=self.shop)
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_cashier).order_by("-id")),
            list(Invoice.objects.filter(order__in=orders).order_by("-id")),
        )

    def test_cashier_no_invoice_queryset(self):
        orders = Order.objects.filter(shop=self.shop1)
        self.assertEqual(
            list(
                self.model_admin.get_queryset(self.request_no_invoice).order_by("-id")
            ),
            list(Invoice.objects.filter(order__in=orders).order_by("-id")),
        )

    def test_cashier_permission_denied_invoice_queryset(self):
        with self.assertRaisesMessage(
            PermissionDenied, "You have no access to this data."
        ):
            self.model_admin.get_queryset(self.request_test_user)

    def test_manager_invoice_queryset(self):
        orders = Order.objects.filter(shop=self.shop)
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_manager).order_by("-id")),
            list(Invoice.objects.filter(order__in=orders).order_by("-id")),
        )

    def test_manager_no_invoice_queryset(self):
        orders = Order.objects.filter(shop=self.shop1)
        self.assertEqual(
            list(
                self.model_admin.get_queryset(self.request_no_invoice1).order_by("-id")
            ),
            list(Invoice.objects.filter(order__in=orders).order_by("-id")),
        )
