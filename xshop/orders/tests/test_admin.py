from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.core.exceptions import PermissionDenied
from model_bakery import baker

from xshop.users.models import Manager, User, GeneralManager, Cashier
from xshop.shops.models import Shop
from ..admin import OrderAdmin
from ..models import Order
from django.urls import reverse
from django.test import Client


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


class OrderAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = OrderAdmin(Order, self.site)
        # shops
        self.shop_test = baker.make(Shop, mobile="01010092182")
        self.shop = baker.make(Shop, mobile="01010092183")
        self.shop1 = baker.make(Shop, mobile="01010092184")

        # orders
        self.order_test = baker.make(Order, shop=self.shop_test)
        self.order = baker.make(Order, shop=self.shop)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)

        self.cashier = baker.make(GeneralManager, mobile="01010092173", shop=self.shop)
        self.password = "testpass123"
        self.cashier.set_password(self.password)
        self.cashier.save()

        self.manager = baker.make(Manager, mobile="01010092186", shop=self.shop)
        self.password = "test123"
        self.cashier.set_password(self.password)
        self.cashier.save()

        self.gm = baker.make(Cashier, mobile="01010092185", shop=self.shop)
        self.password_gm = "testpass1234"
        self.gm.set_password(self.password_gm)
        self.gm.save()

        self.cashier1 = baker.make(Cashier, mobile="01010092188", shop=self.shop1)
        self.manager1 = baker.make(Manager, mobile="01010092189", shop=self.shop1)

        self.test_user = baker.make(User, mobile="01010092175")
        self.password_user = "testpass12345"
        self.test_user.set_password(self.password_gm)
        self.test_user.save()

        # requests

        self.request_super = MockRequest()
        self.request_super.user = self.superuser

        self.request_manager = MockRequest()
        self.request_manager.user = self.manager

        self.request_no_order1 = MockRequest()
        self.request_no_order1.user = self.manager1
        self.request_cashier = MockRequest()
        self.request_cashier.user = self.cashier

        self.request_gm = MockRequest()
        self.request_gm.user = self.gm

        self.request_no_order = MockRequest()
        self.request_no_order.user = self.cashier1

        self.request_test_user = MockRequest()
        self.request_test_user.user = self.test_user

        # url
        self.client = Client()
        self.url = reverse("admin:orders_order_add")

        # attr values

    def test_superuser_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_super).order_by("-id"),
            Order.objects.all().order_by("-id"),
        )

    def test_manager_order_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_manager).order_by("-id")),
            list(Order.objects.filter(shop=self.shop).order_by("-id")),
        )

    def test_manager_no_order_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_no_order).order_by("-id")),
            list(Order.objects.filter(shop=self.shop1).order_by("-id")),
        )

    def test_get_add_order_page_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)

    def test_get_add_order_page_cashier(self):
        self.client.login(mobile=self.cashier.mobile, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_get_add_order_page_gm(self):
        self.client.login(mobile=self.gm.mobile, password=self.password_gm)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_get_add_order_page_user(self):
        self.client.login(mobile=self.test_user.mobile, password=self.password_user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_cashier_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_cashier).order_by("-id"),
            Order.objects.filter(shop=self.shop).order_by("-id"),
        )

    def test_gm_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_gm).order_by("-id"),
            Order.objects.filter(shop=self.shop).order_by("-id"),
        )

    def test_cashier_no_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_no_order).order_by("-id"),
            Order.objects.filter(shop=self.shop1).order_by("-id"),
        )

    def test_cashier_permission_denied_order_queryset(self):
        with self.assertRaisesMessage(
            PermissionDenied, "You have no access to this data."
        ):
            self.model_admin.get_queryset(self.request_test_user)
