from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group
from django.test import RequestFactory, TestCase
from model_bakery import baker
from django.urls import reverse
from django.test import Client

from xshop.users.admin import CustomerAdmin, UserAdmin, DataEntryClerkAdmin
from xshop.users.forms import UserChangeForm
from xshop.users.models import Customer, User, GeneralManager, DataEntryClerk
from xshop.shops.models import Shop
from xshop.core.utils import UserGroup


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


class UserAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = UserAdmin(User, self.site)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)
        self.test_user = baker.make(User, mobile="01010092182")

        # request
        self.request = MockRequest()
        self.request.user = self.superuser

        # attr values
        self.superuser_user_list_display = (
            "id",
            "mobile",
            "email",
            "name",
            "roles",
            "is_staff",
            "is_active",
        )
        self.superuser_list_filter = ("is_staff", "is_active")
        self.readonly_fields = ()

    def test_superuser_user_admin_str(self):
        self.assertEqual(str(self.model_admin), "users.UserAdmin")

    def test_superuser_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request).order_by("-id")),
            list(User.objects.all().order_by("-id")),
        )

    def test_superuser_change_form(self):
        # we are trying to access a form that never exists
        self.request.user = self.superuser
        form = self.model_admin.form(self.request)
        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, UserChangeForm))

    def test_superuser_list_display(self):
        self.assertEqual(
            self.model_admin.get_list_display(self.request),
            self.superuser_user_list_display,
        )

    def test_superuser_list_display_links(self):
        superuser_user_list_display_links = ("id", "mobile")
        self.assertEqual(
            self.model_admin.get_list_display_links(
                self.request, self.superuser_user_list_display
            ),
            superuser_user_list_display_links,
        )

    def test_superuser_list_filter(self):
        self.assertEqual(
            self.model_admin.get_list_filter(self.request),
            self.superuser_list_filter,
        )

    def test_superuser_search_fields(self):
        self.assertEqual(
            self.model_admin.get_search_fields(self.request),
            ("mobile", "email", "name"),
        )

    def test_superuser_change_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_fields(self.request, self.test_user)),
            ("mobile", "password"),
        )

    def test_superuser_exclude_fields(self):
        self.request.user = self.superuser
        self.assertEqual(self.model_admin.get_exclude(self.request), None)

    def test_superuser_read_only_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            self.model_admin.get_readonly_fields(self.request), self.readonly_fields
        )

    def test_superuser_actions(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_actions(self.request).keys()),
            ("delete_selected",),
        )

    # NOTE ::: These Are example of tests for admin panel in django
    # We're going to follow this. We don't need to test all of them
    # we'll just test attributes that need to be present or change
    # based on user types in the future


class CustomerAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = CustomerAdmin(Customer, self.site)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)
        self.customer = baker.make(Customer, mobile="01010092182")

        # request
        self.request = MockRequest()
        self.request.user = self.superuser

        # attr values
        self.superuser_user_list_display = (
            "id",
            "mobile",
            "email",
            "name",
            "roles",
            "is_staff",
            "is_active",
        )
        self.superuser_list_filter = ("is_staff", "is_active")
        self.readonly_fields = tuple()

    def test_superuser_user_admin_str(self):
        self.assertEqual(str(self.model_admin), "users.CustomerAdmin")

    def test_superuser_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request).order_by("-id")),
            list(Customer.objects.all().order_by("-id")),
        )

    def test_superuser_change_form(self):
        # we are trying to access a form that never exists
        self.request.user = self.superuser
        form = self.model_admin.form(self.request)
        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, UserChangeForm))

    def test_superuser_list_display(self):
        self.assertEqual(
            self.model_admin.get_list_display(self.request),
            self.superuser_user_list_display,
        )

    def test_superuser_list_display_links(self):
        superuser_user_list_display_links = ("id", "mobile")
        self.assertEqual(
            self.model_admin.get_list_display_links(
                self.request, self.superuser_user_list_display
            ),
            superuser_user_list_display_links,
        )

    def test_superuser_list_filter(self):
        self.assertEqual(
            self.model_admin.get_list_filter(self.request),
            self.superuser_list_filter,
        )

    def test_superuser_search_fields(self):
        self.assertEqual(
            self.model_admin.get_search_fields(self.request),
            ("mobile", "email", "name"),
        )

    def test_superuser_change_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_fields(self.request, self.customer)),
            ("mobile", "email", "name", "password"),
        )

    def test_superuser_exclude_fields(self):
        self.request.user = self.superuser
        self.assertEqual(self.model_admin.get_exclude(self.request), None)

    def test_superuser_read_only_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            self.model_admin.get_readonly_fields(self.request), self.readonly_fields
        )

    def test_superuser_actions(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_actions(self.request).keys()),
            ("delete_selected",),
        )


class DECAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = DataEntryClerkAdmin(DataEntryClerk, self.site)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)

        self.shop = baker.make(Shop, mobile="01010092183")
        self.gm = baker.make(GeneralManager, mobile="01010092183", shop=self.shop)
        self.password_gm = "testpass1234"
        self.gm.set_password(self.password_gm)
        self.gm.save()

        self.DEC = baker.make(DataEntryClerk, mobile="01010092143", shop=self.shop)

        self.shop1 = baker.make(Shop, mobile="01010092483")
        self.DEC1 = baker.make(DataEntryClerk, mobile="01010592143", shop=self.shop)

        self.test_user = baker.make(User, mobile="01010092182")
        self.password_user = "testpass12345"
        self.test_user.set_password(self.password_gm)
        self.test_user.save()

        # request
        self.request = MockRequest()
        self.request.user = self.superuser

        self.request_gm = MockRequest()
        self.request_gm.user = self.gm

        # attr values
        self.superuser_user_list_display = (
            "id",
            "mobile",
            "email",
            "name",
            "roles",
            "is_staff",
            "is_active",
        )
        self.superuser_list_filter = ("is_staff", "is_active")
        self.readonly_fields = ()

        # url
        self.client = Client()
        self.url = reverse("admin:users_dataentryclerk_add")

    def test_get_add_DEC_page_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)

    def test_get_add_DEC_page_gm(self):
        self.client.login(mobile=self.gm.mobile, password=self.password_gm)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_get_add_DEC_page_user(self):
        self.client.login(mobile=self.test_user.mobile, password=self.password_user)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_superuser_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request).order_by("-id")),
            list(DataEntryClerk.objects.all().order_by("-id")),
        )

    def test_gm_queryset(self):
        g = Group.objects.get(name=UserGroup.DATA_ENTRY_CLERK.title())
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request_gm).order_by("-id")),
            list(User.objects.filter(shop=self.shop, groups=g.id).order_by("-id")),
        )

    def test_superuser_change_form(self):
        # we are trying to access a form that never exists
        self.request.user = self.superuser
        form = self.model_admin.form(self.request)
        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, UserChangeForm))

    def test_superuser_list_display(self):
        self.assertEqual(
            self.model_admin.get_list_display(self.request),
            self.superuser_user_list_display,
        )

    def test_superuser_list_display_links(self):
        superuser_user_list_display_links = ("id", "mobile")
        self.assertEqual(
            self.model_admin.get_list_display_links(
                self.request, self.superuser_user_list_display
            ),
            superuser_user_list_display_links,
        )

    def test_superuser_list_filter(self):
        self.assertEqual(
            self.model_admin.get_list_filter(self.request),
            self.superuser_list_filter,
        )

    def test_superuser_search_fields(self):
        self.assertEqual(
            self.model_admin.get_search_fields(self.request),
            ("mobile", "email", "name"),
        )

    def test_superuser_change_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_fields(self.request, self.test_user)),
            ("mobile", "password"),
        )

    def test_superuser_exclude_fields(self):
        self.request.user = self.superuser
        self.assertEqual(self.model_admin.get_exclude(self.request), None)

    def test_superuser_read_only_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            self.model_admin.get_readonly_fields(self.request), self.readonly_fields
        )

    def test_superuser_actions(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_actions(self.request).keys()),
            ("delete_selected",),
        )
