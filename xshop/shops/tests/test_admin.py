from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from model_bakery import baker
from django.urls import reverse
from django.test import Client

from xshop.users.models import User, GeneralManager
from xshop.shops.models import Shop
from xshop.shops.admin import ShopAdmin


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
        self.model_admin = ShopAdmin(Shop, self.site)

        # shops
        self.shop_test = baker.make(Shop, mobile="01010092182")
        self.shop = baker.make(Shop, mobile="01010092183")
        self.shop1 = baker.make(Shop, mobile="01010092184")

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)

        self.gm = baker.make(GeneralManager, mobile="01010092183", shop=self.shop)
        self.password_gm = "testpass1234"
        self.gm.set_password(self.password_gm)
        self.gm.save()

        self.test_user = baker.make(User, mobile="01010092185")
        self.password_user = "testpass12345"
        self.test_user.set_password(self.password_gm)
        self.test_user.save()

        # requests
        self.request_super = MockRequest()
        self.request_super.user = self.superuser

        self.request_gm = MockRequest()
        self.request_gm.user = self.gm

        self.request_test_user = MockRequest()
        self.request_test_user.user = self.test_user

        # url
        self.client = Client()
        self.url = reverse("admin:shops_shop_add")

        # attr values

    def test_get_add_order_page_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)

    def test_get_add_order_page_gm(self):
        self.client.login(mobile=self.gm.mobile, password=self.password_gm)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_get_add_order_page_user(self):
        self.client.login(mobile=self.test_user.mobile, password=self.password_user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_superuser_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_super).order_by("-id"),
            Shop.objects.all().order_by("-id"),
        )

    def test_gm_order_queryset(self):
        self.assertQuerysetEqual(
            self.model_admin.get_queryset(self.request_gm).order_by("-id"),
            Shop.objects.filter(id=self.shop.id).order_by("-id"),
        )
