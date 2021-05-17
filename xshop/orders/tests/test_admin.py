from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.core.exceptions import PermissionDenied
from model_bakery import baker

from xshop.users.models import Manager, User
from ...shops.models import Shop
from ..admin import OrderAdmin
from ..models import Order


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
        self.user = baker.make(
            User,
            mobile="01010092181",
            name="Ahmed Loay Shahwan",
        )
        # shops
        self.shop_test = baker.make(Shop, mobile="01010092182")
        self.shop = baker.make(Shop, mobile="01010092183")
        self.shop1 = baker.make(Shop, mobile="01010092184")

        # users
        self.superuser = baker.make(User, mobile="01010092187", is_superuser=True)
        self.manager = baker.make(Manager, mobile="01010092183", shop=self.shop)
        self.manager1 = baker.make(Manager, mobile="01010092184", shop=self.shop1)

        # Order
        self.Order_test = baker.make(Order, user=self.superuser, shop=self.shop_test)
        self.Order = baker.make(Order, user=self.manager, shop=self.shop)

        self.test_user = baker.make(User, mobile="01010092185")

        # requests
        self.request_super = MockRequest()
        self.request_super.user = self.superuser

        self.request_manager = MockRequest()
        self.request_manager.user = self.manager

        self.request_no_order = MockRequest()
        self.request_no_order.user = self.manager1

        self.request_test_user = MockRequest()
        self.request_test_user.user = self.test_user

        # attr values

    def test_superuser_order_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_super).order_by("-id")),
            list(Order.objects.all().order_by("-id")),
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

    def test_manager_permission_denied_order_queryset(self):
        with self.assertRaisesMessage(
            PermissionDenied, "You have no access to this data."
        ):
            self.model_admin.get_queryset(self.request_test_user)
