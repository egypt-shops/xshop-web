from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.core.exceptions import PermissionDenied
from model_bakery import baker

from xshop.users.models import GeneralManager, User
from ...shops.models import Shop
from ..admin import ProductAdmin
from ..models import Product


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


class ProductAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = ProductAdmin(Product, self.site)

        # shops
        self.shop_test = baker.make(Shop, mobile="01010092182")
        self.shop = baker.make(Shop, mobile="01010092183")
        self.shop1 = baker.make(Shop, mobile="01010092184")

        # product
        self.product_test = baker.make(Product, name="superuser_p", shop=self.shop_test)
        self.product = baker.make(Product, name="manager_p", shop=self.shop)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)
        self.manager = baker.make(GeneralManager, mobile="01010092183", shop=self.shop)
        self.manager1 = baker.make(
            GeneralManager, mobile="01010092184", shop=self.shop1
        )
        self.test_user = baker.make(User, mobile="01010092185")

        # requests
        self.request_super = MockRequest()
        self.request_super.user = self.superuser

        self.request_manager = MockRequest()
        self.request_manager.user = self.manager

        self.request_no_product = MockRequest()
        self.request_no_product.user = self.manager1

        self.request_test_user = MockRequest()
        self.request_test_user.user = self.test_user

        # attr values

    def test_superuser_product_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_super).order_by("-id")),
            list(Product.objects.all().order_by("-id")),
        )

    def test_manager_product_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_manager).order_by("-id")),
            list(Product.objects.filter(shop=self.shop).order_by("-id")),
        )

    def test_manager_no_product_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_no_product)),
            list(Product.objects.filter(id=0)),
        )

    def test_manager_permission_denied_product_queryset(self):
        with self.assertRaisesMessage(
            PermissionDenied, "You have no access to this data."
        ):
            self.model_admin.get_queryset(self.request_test_user)
